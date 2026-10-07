#!/usr/bin/env python3
#
# sync_google_sheets.py
# 
# [概要]
#
#
#
#
#

import ezsheets

from logging import getLogger
import os

logger = getLogger(__name__)


class SyncGoogleSheets:
    def __init__(self, json_path, sheets_title):
        ezsheets.init(json_path)
        self.ss = ezsheets.Spreadsheet(
            self._get_sheets_id(sheets_title)
        )

    def _get_sheets_id(self, sheets_title):
        '''
        [概要]
        シート名(ファイル名)を受け取り，対応するシートIDを取得して返す関数．

        Arg:
            sheets_title:
        '''
        try:
            all_spreadsheets = ezsheets.listSpreadsheets()

            for spreadsheet_id, spreadsheet_title in all_spreadsheets.items():
                if spreadsheet_title == sheets_title:
                    logger.debug(
                        f"{sheets_title}に一致するIDを取得: \n{spreadsheet_id}"
                    )
                    return spreadsheet_id

            return None

        except Exception as e:
            logger.error(
                f"シートのID取得中に予期せぬエラーが発生しました: {e}"
            )
            return None

    def get_all_data(self, ws_name):
        '''
        '''
        try:
            worksheet = self.ss[ws_name]

            all_data = worksheet.getRows()

            logger.info(
                f"{ws_name}から全てのデータを取得しました"
            )
            return all_data

        except Exception as e:
            logger.error(
                f"{ws_name}からデータ取得時に予期せぬエラーが発生しました: {e}"
            )

    def adjust_data(self, ws_name, start_row, end_row):
        '''
        '''
        try:
            all_data = self.get_all_data(ws_name)

            adjust_data = all_data[start_row -1 : end_row]

            logger.info(
                f"データを必要な量に調整しました: \n{adjust_data}"
            )
            return adjust_data

        except Exception as e:
            logger.error(
                f"データの調整時に予期せぬエラーが発生しました: {e}"
            )
            return None

    def copy_worksheet(self, ws_name, new_ws_name):
        '''
        '''
        if new_ws_name in self.ss.sheetTitles:
            self.delete_worksheet(ws_name)
            logger.error(
                f"' {new_ws_name} 'という名前のワークシートはすでに存在します"
            )
            
        try:
            worksheet = self.ss[ws_name]
            worksheet.copyTo(self.ss)

            new_sheet = self.ss[f"{ws_name} のコピー"]
            new_sheet.title = new_ws_name

            logger.info(
                f"{new_ws_name}という名前のワークシートを複製しました"
            )
            return new_sheet
        
        except Exception as e:
            logger.error(
                f"{ws_name}を複製中に予期せぬエラーが発生しました: {e}"
            )
            return None

    def delete_worksheet(self, ws_name):
        '''
        '''
        try:
            logger.debug("=== delete_worksheet() 実行開始 ===")
            for worksheet in self.ss.sheets:
                if worksheet.title == ws_name:
                    worksheet.delete()

            logger.debug("=== delete_worksheet() 正常に動作完了 ===")

        except Exception as e:
            logger.error(
                f"ワークシートの削除中に予期せぬエラーが発生しました: {e}"
            )

    def write_to_cell(self, use_sheet, num_cell, write_data):
        '''
        '''
        try:
            logger.debug("=== write_to_cell() を実行開始 ===")
            use_sheet[num_cell] = write_data

            logger.debug("=== write_to_cell() を正常に動作終了 ===")

        except Exception as e:
            logger.error(
                f"セルへの書き込み中に予期せぬエラーが発生しました: {e}"
            )


def apu_math(json_path):
    sync_sheets = SyncGoogleSheets(json_path, "【駆けこみ寺】勤務表")
    sync_sheets.adjust_data("R7.10", 1, 55)


def kai(json_path):
    sync_sheets = SyncGoogleSheets(json_path, "PT業務月報（吉田　快）")
    sync_sheets.delete_worksheet("sample_from_python")
    new_sheet = sync_sheets.copy_worksheet("ひな形", "sample_from_python")
    sync_sheets.write_to_cell(new_sheet, "C8", "10")
    
        
if __name__ == "__main__":
    from setup_logging import setup_logging

    setup_logging("../.config/logging_config.yml")

    json_path = "../.config/apu/client_secret.json"
    kai(json_path)
