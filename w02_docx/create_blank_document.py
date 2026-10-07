#!/usr/bin/env python3
#
# create_blank_document.py
#
# [概要]
# Documentオブジェクトを使って
# 白紙のドキュメントファイルを作成し，
# 指定のフォルダに保存するプログラム．
#

import docx
import os

# 出力用のディレクトリ名とファイル名を定義
OUTPUT_DIR = "./output"
OUTPUT_DOC = "output.docx"

# 作成したドキュメントを保存するための相対パスを定義
output_path = os.path.join(
    OUTPUT_DIR,
    OUTPUT_DOC
)

# ドキュメントオブジェクトを定義
document = docx.Document()

# 出力用のディレクトリを作成
os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

# 相対パスを参照して白紙(空)のドキュメントファイルを保存
document.save(output_path)

print("白紙のドキュメントファイルを作成しました．")
