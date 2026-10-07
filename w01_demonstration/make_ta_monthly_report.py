#!/usr/bin/env python3
#
# make_ta_monthly_report.py
# 
# [概要]
#
#
#
#
#

from features.excel_editor import ExcelEditor
from features.datetime_manager import DateTimeManager
from features.sync_google_calendar import SyncGoogleCalendar

from datetime import datetime
from logging import getLogger
import os

logger = getLogger(__name__)


class MakeTAMonthlyReport:
    def __init__(self,
                 input_book,
                 output_book,
                 token_path,
                 json_path,
                 num_sheet=1):
        self.excel_editor = ExcelEditor(
            input_book, output_book, num_sheet=num_sheet
        )
        self.datetime_manager = DateTimeManager()
        self.sync_calendar = SyncGoogleCalendar(
            token_path, json_path
        )
        self.base_date = datetime.today()

    def _get_event_list(self, event_title):
        '''
        [概要]
        GoogleCalendar API経由でイベントタイトルと一致する情報を取得する関数．
        検索範囲は大学の講義時間と重なる8時半 ~ 18時の間．
        かつ，実行日を起点として1ヶ月分のイベントを検索する．

        Arg:
            event_title: カレンダーに追加済みのイベント名
        　　　　　　　　例: TA(Python プログラミング2)
        
        Return:
            event_list: API経由で取得したイベント情報一覧．
                        リストに内包されているが，実際に扱う中身はJSON．
        '''
        try:
            first_date, last_date = self.datetime_manager.get_month_range(
                self.base_date
            )
            first_iso = self.datetime_manager.convert_isoformat(
                first_date, "08:30"
            )
            last_iso = self.datetime_manager.convert_isoformat(
                last_date, "18:00"
            )
            
            event_list = self.sync_calendar.get_event_list(
                event_title, first_iso, last_iso
            )

            logger.info(
                f"{event_title}に該当するイベント情報を取得しました: \n"
            )
            return event_list

        except Exception as e:
            logger.error(
                f"イベントのリストを取得する際にエラーが発生しました: {e}"
            )

    def _convert_event_dates(self, event_title):
        '''
        [概要]
        _get_event_list(event_title)メソッドで取得したイベントリストの中から
        実際にイベントに参加する日時を取得し，TA業務月報へ書き込む際の
        形式へ変換してから，改めてリストに格納する関数．

        Arg:
            event_title: _get_event_list(event_title)を動かすための引数

        Return:
            event_dates: イベントの日付だけを格納したリスト．日付はstr型．
        '''
        try:
            event_list = self._get_event_list(event_title)
            event_dates = []
            for event in event_list:
                event_date = datetime.fromisoformat(
                    event["start"]["dateTime"]
                )

                event_dates.append(
                    event_date.strftime("%-m月%-d日")
                )

            logger.info(
                f"イベントの日付情報を変換しました: {len(event_dates)}件"
            )
            return event_dates

        except Exception as e:
            logger.error(
                f"イベント日の形式変換時に予期せぬエラーが発生しました: {e}"
            )

    def _convert_dates(self, date_list):
        '''
        [概要]
        str型で渡された日付をdatetime型へ変換して新しいリストへ格納する関数．
        なお，別関数実装により今回は出番なし．

        Arg:
            date_list: str型の日付データが内包されたリスト．

        Return:
            converted_date_list: datetime型へ変換した日付データを内包したリスト
        '''
        converted_date_list = []
        try:
            for date in date_list:
                converted_date_list.append(
                    self.datetime_manager.convert_dtformat(date)
                )

            return converted_date_list

        except Exception as e:
            logger.error(
                f"日付データの処理中に予期せぬエラーが発生しました: {e}"
            )

    def _write_work_month(self, cell_num="B2"):
        '''
        [概要]
        業務月報に従事した月を書き込む関数．
        従事した月の判定はself.base_date(実行した日)でおこなう．

        Arg:
            cell_num: write_to_cell()を動かすための引数．
                     入力するセルは不動なので，デフォルト引数を設定
        '''
        try:
            self.excel_editor.write_to_cell(
                cell_num, self.base_date.strftime("%m")
            )
            logger.info(
                "業務月報に従事した月を書き込みました．"
            )

        except Exception as e:
            logger.error(
                f"従事月を書き込み中に予期せぬエラーが発生しました: {e}"
            )

    def _write_student_num(self, cell_num="C4", student_num="M26D003"):
        '''
        [概要]
        業務月報に学籍番号を書き込む関数．
        
        Args:
            cell_num: write_to_cell()を動かすための引数．
                     入力するセルは不動なので，デフォルト引数を設定
            student_num: 固定ユーザなので，自分の学籍番号をデフォルト引数に設定
        '''
        try:
            self.excel_editor.write_to_cell(
                cell_num, student_num
            )
            logger.info(
                "業務月報に学籍番号を書き込みました．"
            )
            
        except Exception as e:
            logger.error(
                f"学籍番号を書き込み中に予期せぬエラーが発生しました: {e}"
            )

    def _write_student_name(self, cell_num="E4", student_name="吉田 快"):
        '''
        [概要]
        業務月報に学生の氏名を書き込む関数．
        
        Args:
            cell_num: write_to_cell()を動かすための引数．
                     入力するセルは不動なので，デフォルト引数を設定
            student_name: 固定ユーザなので，自分の氏名をデフォルト設定．
        '''
        try:
            self.excel_editor.write_to_cell(
                cell_num, student_name
            )
            logger.info(
                "業務月報に氏名を書き込みました"
            )

        except Exception as e:
            logger.error(
                f"氏名を書き込み中に予期せぬエラーが発生しました: {e}"
            )

    def _write_teacher_name(self, cell_num="E6", teacher_name="山口 高康"):
        '''
        [概要]
        業務月報に講義の担当教官名を書き込む関数．
        
        Args:
            cell_num: write_to_cell()を動かすための引数．
                     入力するセルは不動なので，デフォルト引数を設定
            teacher_name: 特に意味はないが，山口先生の氏名をデフォルトに設定
        '''
        try:
            self.excel_editor.write_to_cell(
                cell_num, teacher_name
            )
            logger.info(
                "業務月報に担当教官名を書き込みました．"
            )

        except Exception as e:
            logger.error(
                f"担当教官名を書き込み中に予期せぬエラーが発生しました: {e}"
            )
            
    def _write_lecture_num(self, cell_num, lecture_num):
        '''
        [概要]
        業務月報に従事した回数を書き込む関数．
        
        Args:
            cell_num: write_to_cell()を動かすための引数．
                     入力するセルは不動なので，デフォルト引数を設定
            lecture_num: 1ヶ月の間に従事した回数を渡す．
        '''
        try:
            self.excel_editor.write_to_cell(
                cell_num, lecture_num
            )
            logger.info(
                "業務月報に講義名を書き込みました．"
            )

        except Exception as e:
            logger.error(
                f"講義番号を書き込み中に予期せぬエラーが発生しました: {e}"
            )

    def _write_lecture_name(self, cell_num, lecture_name):
        '''
        [概要]
        業務月報に従事した講義の名前を書き込む関数．
        
        Args:
            cell_num: write_to_cell()を動かすための引数．
                     入力するセルは不動なので，デフォルト引数を設定
            lecture_name: 従事した講義の名前を引数で渡す
        '''
        try:
            self.excel_editor.write_to_cell(
                cell_num, lecture_name
            )

        except Exception as e:
            logger.error(
                f"講義名を書き込み中に予期せぬエラーが発生しました: {e}"
            )

    def _write_date_implemented(self, cell_num, date):
        '''
        [概要]
        業務月報に実際に従事した日付を書き込む関数．
        ＊別関数実装により，日付を書き込む際に形式をする工程を削除．
        なお，名残としてコメントアウトして残している．

        Args:
            cell_num: write_to_cell()を動かすための引数．
                     入力するセルは不動なので，デフォルト引数を設定
            date: 従事した日付を渡す．
        '''
        try:
            #self.excel_editor.write_to_cell(
            #    cell_num, date.strftime("%m月%-d日")
            #)
            self.excel_editor.write_to_cell(
                cell_num, date
            )
            logger.info(
                "業務月報に従事した日付を書き込みました"
            )
            
        except Exception as e:
            logger.error(
                f"日付入力中に予期せぬエラーが発生しました: {e}"
            )

    def _write_time_implemented(self, cell_num, work_time):
        '''
        [概要]
        業務月報に従事した時間(例: 2限)を書き込む関数．
        
        Args:
            cell_num: write_to_cell()を動かすための引数．
                     入力するセルは不動なので，デフォルト引数を設定
            work_time: 従事した時間を引数で渡す．
        '''
        try:
            self.excel_editor.write_to_cell(
                cell_num, work_time
            )
            logger.info(
                "業務月報に従事した時間を書き込みました．"
            )
            
        except Exception as e:
            logger.error(
                f"日付入力中に予期せぬエラーが発生しました: {e}"
            )

    def write_all(self,
                  title,
                  teacher_name,
                  lecture_num,
                  lecture_name,
                  work_time):
        '''
        [概要]
        別関数を実行して，業務月報に必要な情報を書き込む関数．
        
        Args:
        ＊実行する別関数側で引数の意味は記述済みのため，割愛
        '''
        try:
            event_dates = self._convert_event_dates(title)
            start_row = 8

            self._write_work_month()
            self._write_student_num()
            self._write_student_name()
            self._write_teacher_name(teacher_name=teacher_name)

            for n, date in enumerate(event_dates):
                self._write_lecture_num(
                    f"C{start_row + n}", lecture_num
                )
                self._write_lecture_name(
                    f"D{start_row + n}", lecture_name)
                self._write_date_implemented(
                    f"E{start_row + n}", date
                )
                self._write_time_implemented(
                    f"G{start_row + n}", work_time
                )
                
            self.excel_editor.write_to_cell(
                "G28", f"{len(event_dates)}"
            )
                
            self.excel_editor.save_workbook()

            logger.info(
                f"{title}のTA従事情報を月報に書き込み，保存が完了しました．"
            )

        except Exception as e:
            logger.error(
                f"データを書き込み中に予期せぬエラーが発生しました: {e}"
            )


def make_pp1():
    input_book = "./input/ta_monthly_work_report.xlsx"
    output_book = "./output/python_programming1.xlsx"
    token_path = "./.config/cps/token_pickle"
    json_path = "./.config/cps/client_secret.json"
    report_maker = MakeTAMonthlyReport(
        input_book, output_book, token_path, json_path
    )

    report_maker.write_all(
        "TA(Python プログラミング1)",
        "鈴木 一哉",
        "経③",
        "Python プログラミングI",
        "2"
    )


def make_pp2():
    input_book = "./input/ta_monthly_work_report.xlsx"
    output_book = "./output/python_programming2.xlsx"
    token_path = "./.config/cps/token_pickle"
    json_path = "./.config/cps/client_secret.json"
    report_maker = MakeTAMonthlyReport(
        input_book, output_book, token_path, json_path
    )

    report_maker.write_all(
        "TA(Python プログラミング2)",
        "山口 高康",
        "経④",
        "Python プログラミングII",
        "4"
    )


def make_microeconomisc():
    input_book = "./input/ta_monthly_work_report.xlsx"
    output_book = "./output/microeconomisc.xlsx"
    token_path = "./.config/cps/token_pickle"
    json_path = "./.config/cps/client_secret.json"
    report_maker = MakeTAMonthlyReport(
        input_book, output_book, token_path, json_path
    )
    
    report_maker.write_all(
        "TA(ミクロ経済学)",
        "嶋崎 善章",
        "教②",
        "ミクロ経済学",
        "4"
    )


if __name__ == "__main__":
    from features.setup_logging import setup_logging

    setup_logging("./.config/logging_config.yml")

    os.makedirs(
        "output", exist_ok=True
    )
    make_pp1()
    make_pp2()
    make_microeconomisc()
