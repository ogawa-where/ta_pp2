#!/usr/bin/env python3
#
# pattern_matching.py
# 
# [概要]
# Regexオブジェクトを作成して，
# 与えられたテキストデータの中から
# 指定のパターンに合うデータを抽出して
# 表示したり，置換したりするプログラム．
#

import re


def detect_pattern(base_pattern, text, mask_pattern=""):
    # Regexオブジェクトを作成
    regex = re.compile(base_pattern)

    # 最初に一致したパターンを取得する
    match = regex.search(text)
    print("--- 最初に一致したパターン ---")
    if match:
        print("search()を使って見つけたパターン: ", match.group())

    # 一致するパターン全てを取得する
    all_matches = regex.findall(text)
    print("--- 一致したパターン(全て) ---")
    print("findall()を使って見つけたパターン: ", all_matches)

    # 一致するパターンを別の文字列に置換する
    new_text = regex.sub(mask_pattern, text)
    print("--- 文字列を置換 ---")
    print(f"sub()を使って置換: {text} -> {new_text}")
    

if __name__ == "__main__":
    # 日付形式
    DATE_PATTERN = r"(20\d{2})/(0[1-9]|1[0-2])/(0[1-9]|[12]\d|3[01])"
    TIME_PATTERN = r"([01]\d|2[0-3]):([0-5]\d)"
    MAIL_PATTERN = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    PHONE_PATTERN = r"(0\d{1,4}-?\d{1,4}-?\d{4})"

    samples = [
        ("日付", DATE_PATTERN, "今日は2025/09/11．明日は2025/09/12．"),
        ("時間", TIME_PATTERN, "おやつは15:00に食べよう．"),
        ("メール", MAIL_PATTERN, "taro@akita-pu.ac.jp宛にメールを出す．"),
        ("電話", PHONE_PATTERN, "010-2345-6789に電話してください．"),
    ]

    for label, pattern, text in samples:
        print(f"\n--- {label}チェック ---")
        detect_pattern(pattern, text, mask_pattern="*MASK*")

    print("--- チェック終了 ---")
