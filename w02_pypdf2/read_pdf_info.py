#!/usr/bin/env python3
#
# read_pdf_info.py
#
# [概要]
# pypdf2モジュールのPdfReaderクラスを使い，
# 参照したPDFファイルのページ数・1ページ目の
# テキストデータを取得して出力するプログラム
#

import PyPDF2
import os

# 参照するディレクトリとPDFファイルを定義
INPUT_DIR = "./input"
PDF_FILE = "sample.pdf"

# ディレクトリとPDFファイルを繋げて相対パスを定義
pdf_path = os.path.join(
    INPUT_DIR,
    PDF_FILE
)
print(f"ファイルパス: {pdf_path}")

# 定義したPDFファイルが存在しているかをチェック
if not os.path.exists(pdf_path):
    print(f"[エラー] 指定されたPDFファイルが存在しません: {pdf_path}")

else:
    print("=== PDFファイルから抽出した情報 ===")
    # pdf_pathを読み込んだreaderオブジェクトを定義
    reader = PyPDF2.PdfReader(pdf_path)

    # ページ数を取得
    num_pages = len(reader.pages)
    print(f"ページ数: {num_pages}")

    # 1ページ目のテキストを抽出
    first_page_text = reader.pages[0].extract_text() if num_pages > 0 else None
    print("\n--- 1ページ目のテキスト情報 ---")
    print(first_page_text)
