#!/usr/bin/env python3
#
# excel_editor.py
# 
# [概要]
#
#
#
#
#

import openpyxl

#from copy_template import copy_template
from features.copy_template import copy_template

from logging import getLogger
from typing import Dict, List
import os

logger = getLogger(__name__)


class ExcelEditor:
    def __init__(self, input_book, output_book, num_sheet=0):
        copy_template(input_book, output_book)
        self.output_path = output_book
        self.workbook = openpyxl.load_workbook(output_book)
        self.worksheet = self._enable_worksheet(num_sheet)

    def _enable_worksheet(self, num_sheet=0):
        try:
            worksheet = self.workbook.worksheets[num_sheet]

            return worksheet

        except Exception as e:
            logger.error(f"ワークシートの有効化に失敗しました: {e}")

    def _copy_worksheet(self, num_sheet=0, sheet_title="copy_sheet"):
        try:
            current_sheet = self._enable_worksheet(num_sheet)
            copy_sheet = self.workbook.copy_worksheet(current_sheet)

            copy_sheet.title = sheet_title

            return copy_sheet

        except Exception as e:
            logger.error(
                f"ワークシートの複製中に予期せぬエラーが発生しました: {e}"
            )

    def write_to_cell(self, num_cell, write_data):
        try:
            logger.debug("=== write_to_cell() 実行開始")
            self.worksheet[num_cell] = write_data

            logger.debug("=== write_to_cell() 正常に動作終了")

        except Exception as e:
            logger.error(
                f"セルへの書き込み中に予期せぬエラーが発生しました: {e}"
            )

    def save_workbook(self):
        self.workbook.save(self.output_path)
        logger.debug("編集記録を保存しました")
        

if __name__ == "__main__":
    "=== 手動テスト ==="
    from setup_logging import setup_logging

    setup_logging("../.config/logging_config.yml")

    logger.debug("=== ExcelEditor 手動テスト開始 ===")
    os.makedirs(
        "output", exist_ok=True
    )
    
    input_book = "../input/ta_monthly_work_report.xlsx"
    output_book = "./output/output.xlsx"
    excel_editor = ExcelEditor(input_book, output_book, num_sheet=1)
    excel_editor.write_to_cell("B2", "10")
    excel_editor.save_workbook()
    
    logger.debug("=== ExcelEditor 手動テスト終了 ===")
