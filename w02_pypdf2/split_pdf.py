#!/usr/bin/env python3
#
# split_pdf.py
#
# [概要]
# PdfReaderクラスとPdfWriterクラスを使い，
# 指定したPDFファイルをページごとに分割して
# 1ページずつ保存するプログラム．
#

import PyPDF2
import os

# 入出力用のディレクトリとファイルを定義
INPUT_DIR = "./input"
OUTPUT_DIR = "./output"

INPUT_FILE = "sample.pdf"

# 入力用の相対パスを定義
input_path = os.path.join(
    INPUT_DIR,
    INPUT_FILE
)

# 出力用のディレクトリを作成(重複しない)
os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

# PDFファイルの読み込み
reader = PyPDF2.PdfReader(input_path)

# ページごとに分割して保存
for i, page in enumerate(reader.pages, start=1):
    writer = PyPDF2.PdfWriter()
    writer.add_page(page)

    # ページナンバーで名前をつける
    output_file = f"page_{i}.pdf"
    output_path = os.path.join(
        OUTPUT_DIR,
        output_file
    )

    with open(output_path, "wb") as pdf:
        writer.write(pdf)

    print(f"[完了] {output_path}に保存しました")

print(f"\n=== {INPUT_FILE}をページごとに分割しました ===")
