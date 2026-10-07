#!/usr/bin/env python3
#
# rotate_pdf.py
#
# [概要]
# pypdf2モジュールのPdfWriterクラスを使い，
# 参照したPDFファイルの任意のページを90度回転
# させるプログラム．
#
# ＊ 回転時の繰り返し処理のためにPdfReaderでページ数を
# 取得している．
#

import PyPDF2
import os

# 入出力用のディレクトリとファイルを定義
INPUT_DIR = "./input"
OUTPUT_DIR = "./output"

INPUT_FILE = "sample.pdf"
OUTPUT_FILE = "rotated_sample.pdf"

# 入出力用の相対パスを定義
input_path = os.path.join(
    INPUT_DIR,
    INPUT_FILE
)

output_path = os.path.join(
    OUTPUT_DIR,
    OUTPUT_FILE
)

# 出力用のディレクトリを作成(重複しない)
os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

# 読み込み用のオブジェクトと編集用オブジェクトを定義
reader = PyPDF2.PdfReader(input_path)
writer = PyPDF2.PdfWriter()

# ページの回転処理(1ページ目だけ)
for i, page in enumerate(reader.pages):
    if i == 0:
        rotated_page = page.rotate(90)
        writer.add_page(rotated_page)

    else:
        writer.add_page(page)

# 新しいPDFファイルとして保存
with open(output_path, "wb") as pdf:
    writer.write(pdf)

print(f"[完了] {output_path}に保存しました")
