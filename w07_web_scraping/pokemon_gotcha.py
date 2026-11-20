#!/usr/bin/env python3
#
# pokemon_gotcha.py
#
# [概要]
# 公式の「ポケモンずかん」
# （https://zukan.pokemon.co.jp/）
# を参照して，好きなポケモンの画像を
# 取得して保存するプログラム．
#
# ＊名前の一部が一致している場合は，
# 　全て保存する．
#


from bs4 import BeautifulSoup
import requests

from features.setup_logging import setup_logging
from features.setup_selenium import setup_driver, driver_wait

from logging import getLogger
from pathlib import Path
import time
import sys

USAGE = "[USAGE] python pokemon_gotcha.py pokemon_name"


# loggingの設定を反映して，専用のロガーを作成
setup_logging()
logger = getLogger(__name__)


def scroll_page(driver, url):
    '''
    [概要]
    driverオブジェクトを使って対象のWebサイトを
    一番下までスクロールする関数．
    '''
    assert isinstance(url, str), "url は文字列型である必要があります"
    
    try:
        logger.info("指定のサイトへアクセスします")
        driver.get(url)
        driver_wait(driver)
        logger.info(
            f"指定のサイトへアクセスできました: {driver.title}"
        )

        logger.info("ブラウザで全ポケモンを表示するためにスクロールを開始")

        last_height = driver.execute_script(
            "return document.body.scrollHeight"
        )

        while True:
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )

            time.sleep(2)

            new_height = driver.execute_script(
                "return document.body.scrollHeight"
            )

            if new_height == last_height:
                logger.info("ページの最下部に到達しました")
                break
            last_height = new_height

        return driver.page_source

    except Exception as e:
        logger.error(
            f"画面のスクロール中にエラーが発生しました: {e}"
        )
        raise


def save_pokedex_html(page_source, save_path):
    '''
    [概要]
    selenium で取得した HTML をローカルに保存する関数
    '''
    assert isinstance(page_source, str), "page_source は文字列にしてください"

    try:
        logger.info("取得したHTMLをローカルに保存します")
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(page_source)
        logger.info("HTMLをローカルに保存しました")
        
        return True

    except Exception as e:
        logger.error(
            f"HTML保存中にエラーが発生しました: {e}"
        )
        raise
    

def make_soup(page_source):
    '''
    [概要]
    指定された url (今回は公式のポケモンずかん) を参照して，
    BeautifulSoup オブジェクト (soup) を作成し，返す関数．

    Arg:
        url (str): 情報を取得したい Webサイトの URL を指定．
    '''
    try:
        logger.info(
            "HTML を読み込んでオブジェクトを作成します"
        )
        soup = BeautifulSoup(
            page_source, "html.parser"
        )
        logger.info(
            "BeautifulSoup オブジェクトを作成しました"
        )

        return soup

    except Exception as e:
        logger.error(
            f"BeautifulSoup オブジェクトの作成時にエラーが発生しました: {e}"
        )
        raise


def found_img_sources(soup, name, tag="img"):
    '''
    [概要]
    取得したい画像のURIを取得する関数．
    ''' 
    try:
        logger.info("指定の画像を見つけます")
        img_tags = soup.select(tag)
        logger.debug(
            f"img_tagsの中身: {len(img_tags)}"
        )
        img_srcs = []
        for img in img_tags:
            alt_text = img.get("alt")

            if alt_text == name:
                logger.info(
                    f"{name}の気配がする・・・"
                )
                time.sleep(2)

                img_src = img.get("src")
                img_srcs.append(img_src)

                if not img_src:
                    logger.warning(
                        f"{name}はここにはいないようだ・・・"
                    )

        return img_srcs

    except Exception as e:
        logger.error(
            f"画像検索中にエラーが発生しました: {e}"
        )
        raise


def gotcha(img_src, save_img_path):
    '''
    [概要]
    画像のURIを指定してダウンロードする関数．
    '''
    try:
        img_url = img_src
        logger.info(
            f"指定の URL へリクエストを送ります: {img_url}"
        )
        img_response = requests.get(img_url)
        img_response.raise_for_status()

        logger.info(
            "ポケモンを見つけました!"
        )

        logger.info(
            "捕獲します!"
        )

        with open(save_img_path, "wb") as f:
            f.write(img_response.content)

        logger.info(
            f"ポケモンを捕獲しました!: {save_img_path}"
        )

        time.sleep(2)
        
        return True

    except Exception as e:
        logger.error(
            f"捕獲に失敗しました: {e}"
        )
        raise


def main(name):
    '''
    [概要]
    定義した別関数を連動させて実行するメインの関数．
    '''
    url = "https://zukan.pokemon.co.jp/"

    input_dir = Path("input")
    pokedex_html_path = input_dir / "pokedex.html"

    save_dir = Path("output")
    save_dir.mkdir(exist_ok=True)

    if not pokedex_html_path.exists():
        logger.info("pokedex.html が存在しません．取得処理を開始します．")
        # driverをグローバル変数としてセット
        driver = setup_driver()
        page_source = scroll_page(driver, url)
        save_pokedex_html(page_source, pokedex_html_path)
        driver.quit()

    else:
        logger.info("既存の pokedex.html を使用します")
        try:
            with open(pokedex_html_path, "r", encoding="utf-8") as f:
                page_source = f.read()

        except Exception as e:
            logger.error(
                f"ローカル HTML の読み込みに失敗しました: {e}"
            )
            raise
        
    soup = make_soup(page_source)
    img_srcs = found_img_sources(soup, name)

    for i, img_src in enumerate(img_srcs):
        img_name = f"pokemon_gotcha_{i+1}.png"
        save_img_path = save_dir / img_name
        time.sleep(10)
        gotcha(img_src, save_img_path)

    logger.info(
        f"{name}を{len(img_srcs)}匹，ゲットだぜ!"
    )


if __name__ == "__main__":
    if len(sys.argv) > 1:
        name = sys.argv[1]
        main(name)
    else:
        logger.info(USAGE)
