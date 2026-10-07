#!/usr/bin/env python3
#
# datetime_maneger.py
# 
# [概要]
# 日時情報の操作を円滑に進めるためのPythonスクリプト．
# 入力された日付データを使い，参照するべき月や週を
# よしなに取得できる．
# なお，日本固有の和暦を取得するために
# 外部モジュールである"datetimeJP"を，
# 該当月の月初日と月末日を取得するために
# "python-dateutil"を導入している．
#

from datetimejp import JDatetime
from dateutil.relativedelta import relativedelta

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from logging import getLogger
import os

logger = getLogger(__name__)


class DateTimeManager:
    def __init__(self, tz="Asia/Tokyo"):
        self.tz = ZoneInfo(key=tz)

        self.weeks = {
            "0": "日",
            "1": "月",
            "2": "火",
            "3": "水",
            "4": "木",
            "5": "金",
            "6": "土"
        }

    def convert_dtformat(self, input_date: str) -> datetime:
        '''
        [概要]
        文字列(str)型で表現された日付データを
        datetime型(%Y-%m-%d HH:MM::SS)へ変換して返す関数．

        Arg:
            input_date(str): (例)"2025-09-25"や"2025/09/25"，"2025年9月25日"

        Return:
            converted_date(datetime): "2025-09-25 00:00:00"のようなデータ
        '''
        date_formats = [
            "%Y-%m-%d",
            "%Y/%m/%d",
            "%Y年%m月%d日"
        ]

        for fmt in date_formats:
            try:
                converted_date = datetime.strptime(input_date, fmt)

                logger.info("型の変換に成功しました")
                return converted_date
                break
        
            except ValueError:
                continue

    def add_time(self, input_date, moment) -> datetime:
        '''
        [概要]
        入力された日付データに時間データを追加した上で，
        datetime型のデータへ変換する関数．
        主に，ISO形式の時間データへ変換する際の前処理として役に立つ．

        Args:
            input_date: 基本的な日付データ．文字列も可．
            moment(str): 型の変換時に挿入する時間データを文字列型で受け取る

        Return:
            converted_date.replace(): 時間データも保持したdatetime型データ．
        '''

        if isinstance(input_date, str):
            converted_date = self.convert_dtformat(input_date)

        else:
            converted_date = input_date
        
        try:
            parts = list(
                map(
                    int, moment.strip().split(":")
                )
            )

            if len(parts) == 2:
                hour, minute = parts
                second = 0

            elif len(parts) ==3:
                hour, minute, second = parts

            else:
                raise ValueError(
                    f"本機能が受け付けられないデータ型です: {input_date}"
                )

            logger.info("時間情報の挿入に成功しました")
            return converted_date.replace(
                hour=hour, minute=minute, second=second
            )

        except Exception as e:
            raise ValueError(
                f"momentのパースに失敗しました: {moment} ({e})"
            )

    def convert_wareki(self, input_date, option="%g%-e") -> str:
        '''
        [概要]
        入力された日付データから和暦を算出する関数

        Args:
            day_date(str or datetime): "2025-06-04"のような形式
            ＊"2025/06/04"や"2025年06月04日"の形式も可
            option (str): 出力される形式を指定する
            デフォルトは"令和X"
        
        ＊  "%g": 昭和，平成，令和
            "%-g", "%#g": S, H, R, s, h, r
            "%e": 01, 02, ..., 99
            "%-e", "%#e": 1, 2, ..., 99

        Return:
            wareki (str): "令和7"のような形式
        '''
        if isinstance(input_date, datetime):
            date = input_date.strftime("%Y-%m-%d")

        elif isinstance(input_date, str):
            date = self.convert_dtformat(input_date).strftime("%Y-%m-%d")

        else:
            raise ValueError("本機能が対応できないデータ型です: {input_date}")

        try:
            datejp = JDatetime.strptime(date, "%Y-%m-%d")

            logger.info("和暦取得用のデータ型へ変換しました")
            return datejp.strftime(option)

        except Exception as e:
            logger.error(
                f"和暦取得時に予期せぬエラーが発生しました: {e}"
            )
            return None

    def convert_week_jp(self, input_date):
        '''
        入力された日付における曜日(日本形式: "月"，"火"...)を取得する

        Arg:
           day_data (str or datetime): これまで同様

        Return:
           self.week_dict[weekday_num]: "月"，"火"など
        '''
        if isinstance(input_date, str):
            date = self.convert_dtformat(input_date)

        else:
            pass

        try:
            weekday_num = str(
                (date.weekday() + 1) % 7
            )

            logger.info("曜日の取得に成功しました")
            return self.weeks[weekday_num]
        
        except Exception as e:
            logger.error(
                f"曜日の取得時に予期せぬエラーが発生しました: {e}"
            )
            return None

    def get_month_range(self, input_date):
        '''
        [概要]
        入力された日付データを参照し，対象となる月の月初日と月末日を
        算出して返す関数

        Arg:
           day_data: これまでと同様
        
        Returns:
           first_date, last_date(datetime): 例 2025-06-01と2025-06-30
        '''
        if isinstance(input_date, str):
            date = self.convert_dtformat(input_date)

        else:
            date = input_date

        try:
            first_date = date.replace(day=1)

            last_date = (
                first_date + relativedelta(months=1)
            ).replace(day=1) - timedelta(days=1)

            logger.info(
                f"{first_date.strftime('%m')}月の月初日と月末日を取得しました)"
            )
            return first_date, last_date

        except Exception as e:
            logger.error(
                f"月初日と月末日の取得時に予期せぬエラーが発生しました: {e}"
            )
            return None

    def get_week_range(self, input_date):
        '''
        [概要]
        入力された日付データを参照し，対象となる週の初め(日)と終わり(土)を
        算出して返す関数

        Arg:
           day_data: これまで同様

        Returns:
           sunday, saturday(datetime): 該当の週の日曜日と土曜日
        '''
        if isinstance(input_date, str):
            date = self.convert_dtformat(input_date)
            
        try:
            days_to_sunday = (date.weekday() + 1) % 7
            sunday = date - timedelta(days=days_to_sunday)
            saturday = sunday + timedelta(days=6)

            logger.info("週初日と週末日の取得に成功しました")
            return sunday, saturday

        except Exception as e:
            logger.error(
                f"週初日と週末日の取得時に予期せぬエラーが発生しました: {e}"
            )
            return None

    def convert_isoformat(self, input_date, moment):
        '''
        [概要]
        Google カレンダーのような外部サービスと連携する際にはISO形式の時間表記
        にする必要がある．
        この関数では，与えられた日付データ(str含む)を
        ISO形式に変換する役割を担う．

        Arg:
            day_data (str or datetime): "2025-06-04"のような形式
            ＊"2025/06/04"や"2025年06月04日"の形式も可
        
        Return:
            iso_data: "2025-06-04T00:00:00+09:00"のような形式
        '''
        try:
            date = self.add_time(input_date, moment)

            if date.tzinfo is None:
                date = date.replace(tzinfo=self.tz)

            logger.info("ISO形式への変換に成功しました")
            return date.isoformat()

        except Exception as e:
            logger.error(
                f"ISO形式への変換時に予期せぬエラーが発生しました: {e}"
            )
            return None


if __name__ == "__main__":
    "--- 手動テスト ---"
    from setup_logging import setup_logging

    setup_logging("../.config/logging_config.yml")
    logger.debug("=== DateTimeManger 手動テスト開始 ===")

    datetime_manager = DateTimeManager()
    
    befores = [
        "2021-8-5",
        "2022-09-25",
        "2023/8/25",
        "2024/10/25",
        "2025年11月1日"
    ]
        
    for before in befores:
        converted_date = datetime_manager.convert_dtformat(before)
        logger.debug(f"{before} -> {converted_date}")
        converted_date = datetime_manager.add_time(before, "18:30")
        logger.debug(f"{before} -> {converted_date}")
        converted_date = datetime_manager.convert_isoformat(before, "20:30")
        logger.debug(f"{before} -> {converted_date}")

        wareki = datetime_manager.convert_wareki(before, option="%-e")
        logger.debug(f"令和'{wareki}'年です")

        week = datetime_manager.convert_week_jp(before)
        logger.debug(f"{before}は'{week}'曜日でした")

        first_date, last_date = datetime_manager.get_month_range(before)
        logger.debug(f"月初日: {first_date}, 月末日: {last_date}")

        first_date, last_date = datetime_manager.get_week_range(before)
        logger.debug(f"週初日: {first_date}, 週末日: {last_date}")
        
    logger.debug("=== DateTimeManager 手動テスト終了 ===")
