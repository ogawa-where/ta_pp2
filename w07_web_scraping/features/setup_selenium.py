#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from features.setup_logging import setup_logging
#from setup_logging import setup_logging

from logging import getLogger

logger = getLogger(__name__)


def setup_driver():
    try:
        logger.info("ChromeDriverのセットアップを開始します")
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = Service(
            ChromeDriverManager().install()
        )

        driver = webdriver.Chrome(
            service=service,
            options=options
        )

        logger.info("ChromeDriverのセットアップが完了しました")

        return driver

    except Exception as e:
        logger.error(
            f"ChromeDriverのセットアップ中にエラーが発生しました: {e}"
        )
        raise


def driver_wait(driver, max_wait_time=10):
    assert isinstance(driver, webdriver.Chrome), "driverオブジェクトが不正です"
    
    try:
        logger.info("ページが読み込まれるまで待機します")

        wait = WebDriverWait(driver, max_wait_time)

        #wait.until(
        #    EC.presence_of_element_located(
        #        (By.ID, tag_id)
        #    )
        #)

        logger.info("ページが読み込まれました")

    except Exception as e:
        logger.error(
            f"ページ読み込み待機中にエラーが発生しました: {e}"
        )
        raise


if __name__ == "__main__":
    setup_logging()

    url = "https://zukan.pokemon.co.jp/"
    driver = setup_driver()
    driver.get(url)

    driver_wait(driver)
    
    logger.debug(
        f"該当サイトのタイトルを取得しました: {driver.title}"
    )
    
    driver.quit()
