#!/usr/bin/env python3
#
# create_new_document.py
#
# [概要]
# Documentオブジェクトを使って
# 見出し・段落・箇条書き・番号付きリストを
# 書き込んだドキュメントファイルを作成する
# プログラム．
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

# 見出しを追加(level=1は一番大きい見出し)
document.add_heading(
    "Python プログラミング2",
    level=1
)

# 段落を追加してテキストを書き込み
document.add_paragraph("最初の段落")
document.add_paragraph(
    "docx モジュールを使って，ドキュメントファイルにテキストを書き込みます"
)

# 箇条書きを追加
document.add_paragraph(
    "りんご",
    style="List Bullet"
)
document.add_paragraph(
    "みかん",
    style="List Bullet"
)
document.add_paragraph(
    "バナナ",
    style="List Bullet"
)

# 番号付きリストを追加
document.add_paragraph(
    "春",
    style="List Number"
)
document.add_paragraph(
    "夏",
    style="List Number"
)
document.add_paragraph(
    "秋",
    style="List Number"
)
document.add_paragraph(
    "冬",
    style="List Number"
)

# 出力用のディレクトリを作成
os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

# 相対パスを参照して白紙(空)のドキュメントファイルを保存
document.save(output_path)

print("ドキュメントファイルを作成しました．")
