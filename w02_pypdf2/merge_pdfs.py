#!/usr/bin/env python3
#
# merge_pdfs.py
#
# [概要]
# PdfMergerクラスを使い，
# 3つのPDFファイルを結合して
# 保存するプログラム．
#

import PyPDF2
import os

# 入出力用のディレクトリとファイルを定義
INPUT_DIR = "./input"
OUTPUT_DIR = "./output"

OUTPUT_FILE = "merged_sample.pdf"

# 結合するためのPDFファイルを取得して，相対パスをリストに格納する
input_files = []
for filename in os.listdir(INPUT_DIR):
    if filename.endswith(".pdf"):
        input_files.append(f"{INPUT_DIR}/{filename}")

# リスト内の順番を並べ替え
input_files.sort(key=str.lower)

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

# 結合用のオブジェクトを定義
merger = PyPDF2.PdfMerger()

# 繰り返し処理を使ってリスト内のPDFファイルを結合
for pdf_path in input_files:
    merger.append(pdf_path)

# 新しいPDFファイルをして保存
with open(output_path, "wb") as pdf:
    merger.write(pdf)

print(f"[完了] {output_path}に保存しました")
