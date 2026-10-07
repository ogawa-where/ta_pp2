#!/usr/bin/env python3
#
# text_extraction.py
#
# [概要]
# 既存のドキュメントファイルから
# テキストデータを取得して表示する
# プログラム．
#

import docx
import os

# ドキュメントファイルを定義
INPUT_DOC = "./input/demo.docx"
docx = docx.Document(INPUT_DOC)

# テキストを取得して出力
print(f"--- {INPUT_DOC}のテキスト情報 ---\n")
for paragraph in docx.paragraphs:
    print(paragraph.text)
