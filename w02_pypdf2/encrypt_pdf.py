#!/usr/bin/env python3
#
# encrypt_pdf.py
#
# [概要]
# PdfReaderクラスとPdfWriterクラスを使い，
# 既存のPDFファイルを複製して，
# 暗号化して保存するプログラム．
#

import PyPDF2
import os

# 入出力用のディレクトリとファイルを定義
INPUT_DIR = "./input"
OUTPUT_DIR = "./output"

INPUT_FILE = "sample.pdf"
OUTPUT_FILE = "encrypted_sample.pdf"

# 暗号化用のパスワード(好きなパスワードに変更可)
PASSWORD = "thanks"

# 入出力用の相対パスを定義
input_path = os.path.join(
    INPUT_DIR,
    INPUT_FILE
)

# 出力用の相対パスを定義
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

# 全ページを追加
for page in reader.pages:
    writer.add_page(page)

# PDFの暗号化処理
writer.encrypt(PASSWORD)

# 暗号化済みPDFを保存する
with open(output_path, "wb") as pdf:
    writer.write(pdf)

print(f"[完了] 暗号化PDFを {output_path} に保存しました．")
print(f"開くときのパスワード: {PASSWORD}")
