#!/usr/bin/env python3
#
# save_pattern.py
# 
# [概要]
# inputディレクトリに保存したlong_text.txtを
# 参照して取得したテキスト情報から，
# メールアドレスと電話番号を抽出し，
# 新規テキストファイルへ保存するプログラム．
#

import re
import os


def read_txt(input_txt):
    '''
    [概要]
    テキストファイルを読み込むための関数

    Args:
        input_txt (str): 入力用テキストファイルを参照するための相対パス

    Return:
        text (str): テキストファイルから取得したテキストデータ
    '''
    with open(input_txt, "r", encoding="utf-8") as txf:
        text = txf.read()

    return text


def detect_pattern(base_pattern, text):
    '''
    [概要]
    パターンマッチしたデータをリストに保存して返す関数

    Args:
        base_pattern (str): 探す対象を示すパターン(今回はメールと電話番号)

    Returns:
        all_matchec (list): パターンマッチしたデータが保存されたリスト
    '''
    regex = re.compile(base_pattern)

    all_matches = regex.findall(text)

    return all_matches


def save_txt(output_txt, mail_list, phone_list):
    '''
    [概要]
    渡されたリストデータの中身を1つずつテキストファイルに書き込む関数

    Args:
        output_txt (str): 保存するテキストファイルの相対パス
        mail_list (list): メールアドレスだけが保存されたリスト
        phone_list (list): 電話番号だけが保存されたリスト

    Returns:
        True
    '''
    with open(output_txt, "w", encoding="utf-8") as txf:
        # メールアドレスを書き込み
        for mail in mail_list:
            txf.write(mail + "\n")

        # 電話番号を書き込み
        for phone in phone_list:
            txf.write(phone + "\n")

    return True


def main_process(input_txt, output_txt, mail_pattern, phone_pattern):
    '''
    [概要]
    定義した関数を順番に動かして，全体を駆動させる関数

    Args:
        input_txt (str): read_text関数を動かすための相対パス
        output_txt (str): save_txt関数を動かすための相対パス
        mail_pattern (str): メールアドレスを示すパターン表記
        phone_pattern (str): 電話番号を示すパターン表記

    Returns:
        None
    '''
    text = read_txt(input_txt)
    mail_list = detect_pattern(mail_pattern, text)
    phone_list = detect_pattern(phone_pattern, text)
    check = save_txt(output_txt, mail_list, phone_list)

    if check == True:
        print(f"{output_txt}を保存しました．")

    else:
        print("問題が発生しました．")

        
if __name__ == "__main__":
    # メールアドレスと電話番号のパターン表記を定義
    MAIL_PATTERN = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    PHONE_PATTERN = r"(0\d{1,4}-?\d{1,4}-?\d{4})"

    # 入出力用の相対パスを定義
    INPUT_TXT = "./input/long_text.txt"
    OUTPUT_DIR = "./output"
    OUTPUT_TXT = "output.txt"

    # 出力用のディレクトリを作成
    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    # 出力用のテキストファイルの相対パスを定義
    output_path = os.path.join(
        OUTPUT_DIR,
        OUTPUT_TXT
    )

    # main_processを動かして，全ての関数を実行
    main_process(
        INPUT_TXT,
        output_path,
        MAIL_PATTERN,
        PHONE_PATTERN
    )
