#!/usr/bin/env python3
#
# insert_table.py
#
# [概要]
# Documentオブジェクトを使って
# 白紙のドキュメントファイルを作成し，
# テーブルとデータを書き込むプログラム．
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

# テーブルを追加(3列 x 4行)
table = document.add_table(
    rows=4,
    cols=3
)
table.style = "Table Grid" # 罫線付きのスタイルに設定

# 1行目をヘッダーにする
hdr_cells = table.rows[0].cells
hdr_cells[0].text = "名前"
hdr_cells[1].text = "学年"
hdr_cells[2].text = "メールアドレス"

# 2行目以降に書き込むサンプルデータを定義
insert_data = [
    ["山田 太郎", "2年", "taro@akita-pu.ac.jp"],
    ["佐藤 花子", "3年", "hanako@akita-pu.ac.jp"],
    ["鈴木 一郎", "1年", "ichiro@akita-pu.ac.jp"]
]

# 繰り返し処理を使ってデータを書き込み
for i, row_data in enumerate(insert_data, start=1):
    row_cells = table.rows[i].cells
    for j, value in enumerate(row_data):
        row_cells[j].text = value

# 出力用のディレクトリを作成
os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

# 相対パスを参照してドキュメントファイルを保存
document.save(output_path)

print("表データ付きドキュメントファイルを作成しました．")
