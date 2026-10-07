#!/usr/bin/env python3
#
# insert_image.py
#
# [概要]
# Documentオブジェクトを使って
# 白紙のドキュメントファイルを作成し，
# 画像を挿入するプログラム．
#

import docx
from docx.shared import Inches
import os

# 挿入するための画像ファイルを定義
INPUT_IMAGE = "./input/python_logo.png"

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

# 相対パスを参照して画像を挿入
document.add_paragraph("ここに画像を挿入します．")
document.add_picture(
    INPUT_IMAGE,
    width=Inches(2.0)
)

# 出力用のディレクトリを作成
os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

# 相対パスを参照してドキュメントファイルを保存
document.save(output_path)

print("画像付きドキュメントファイルを作成しました．")
