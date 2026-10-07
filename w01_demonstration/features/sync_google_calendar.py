#!/usr/bin/env python3
#
# sync_google_calendar.py
#
# [概要]
#
#
#
#
#

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from logging import getLogger
import os
import pickle

logger = getLogger(__name__)


class SyncGoogleCalendar:
    def __init__(self, token_path, json_path, calendar_id="primary"):
        '''
        [概要]
        SCOPESとserviceをクラス内で再利用可能な変数で定義

        Args:
            token_path (str): _creds_refreshメソッドで使用する
            json_path (str): _creds_refreshメソッドで使用する
        
        '''
        self.SCOPES = [
            "https://www.googleapis.com/auth/calendar"
        ]

        creds = self._creds_refresh(token_path, json_path)
        self.service = build(
            "calendar",
            "v3",
            credentials=creds,
        )

        self.calendar_id = calendar_id

    def _creds_refresh(self, token_path: str, json_path: str):
        '''
        [概要]
        認証情報をロードあるいは更新する

        Args:
            token_path (str): トークンファイルのパス
            json_path (str): 認証情報ファイルのパス

        Returns:
            creds | None: 認証情報オブジェクト．認証に失敗した場合はNone

        '''
        token_path = token_path
        creds = None

        if os.path.exists(token_path):
            with open(token_path, "rb") as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())

            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    json_path,
                    self.SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open(token_path, "wb") as token:
                pickle.dump(creds, token)

        return creds

    def get_calendar_id(self, calendar_name: str):
        '''
        [概要]
        指定するカレンダーのIDを取得する

        Args:
            calendar_name (str): 使用するカレンダーの名前

        Returns:
            calendar_id (str): 対象のカレンダーのID
        
        ＊通常は自分のカレンダーを示す"primary"をIDとして用いる
        
        '''
        calendar_list = self.service.calendarList().list().execute()

        for calendar_entry in calendar_list.get("items", []):
            access_role = calendar_entry.get("accessRole")
            summary = calendar_entry.get("summary")
            calendar_id = calendar_entry.get("id")

            if access_role in ("owner", "writer") and summary == calendar_name:
                return calendar_id

            else:
                calendar_id = "primary"
                return calendar_id

    def get_event_id(self,  event_name, start_iso, end_iso):
        '''
        [概要]
        カレンダーIDとイベント名，対象の日付を使ってイベントのIDを取得する

        Args:
            event_name (str): 検索対象に設定するイベントの名前
            scheduled_date (str): イベントが予定されている日付

        Returns:
            event_id (str): 対象としたイベントのID

        '''
        if not self.service:
            logger.error("サービスが初期化されていません。処理を中止します。")
            return None
        
        try:
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                q=event_name,
                timeMin=start_iso,
                timeMax=end_iso,
                maxResults=5,
                singleEvents=True,
                orderBy="startTime",
            ).execute()
            events = events_result.get("items", [])

            if not events:
                logger.info(f"---検索条件と一致するイベントは見つからない---")
                return None
            
            for event in events:
                if event.get("summary") == event_name:
                    event_id = event["id"]
                    return event_id

            logger.info("名前が完全に一致するイベントは見つかりませんでした")
            return None

        except TypeError as te:
            logger.error(f"APIリクエスト中にエラーが発生しました: {te}")
            return None

        except Exception as e:
            logger.error(f"予期せぬエラーが発生しました: {e}")
            return None

    def delete_event(self, event_id):
        '''
        [概要]
        カレンダーIDとイベントIDを参照して，カレンダー内に存在したイベントを
        削除する．

        '''
        if not self.service:
            logger.error(
                "---サービスが初期化されていません．処理を中止します---"
            )
            return False

        if not event_id:
            logger.error(
                "---イベントIDが指定されていません．処理を中止します---"
            )
            return False

        try:
            self.service.events().delete(
                calendarId=self.calendar_id,
                eventId=event_id,
            ).execute()
            logger.info(f"削除したイベントID: {event_id}")
            return True

        except TypeError as te:
            logger.error(f"イベントの削除中にAPIエラーが発生しました: {te}")
            return False

        except Exception as e:
            logger.error(
                f"イベントの削除中に予期せぬエラーが発生しました: {e}"
            )
            return False

    def add_event(self, start_iso_date, end_iso_date, summary, location):
        '''
        [概要]
        指定された日時・タイトル・場所でGoogleカレンダーにイベントを追加する．
        
        Args:
            start_iso_date (str): イベント開始日時（
                                  ISO形式，例："2025-06-07T10:00:00"
                                  ）．
            end_iso_date (str): イベント終了日時（ISO形式）．
            summary (str): イベントのタイトル．
            location (str): イベントの場所．

        Returns:
            bool: イベントの追加に成功すれば True，失敗すれば False を返す．
        '''
        event = {
            "summary": f"{summary}",
            "location": f"{location}",
            "description": "",
            "start": {
                "dateTime": f"{start_iso_date}",
                "timeZone": "Asia/Tokyo",
            },
            "end": {
                "dateTime": f"{end_iso_date}",
                "timeZone": "Asia/Tokyo",
            },
        }

        try:
            event_result = self.service.events().insert(
                calendarId=self.calendar_id,
                body=event,
            ).execute()
            return True

        except Exception as e:
            logger.error(f"イベントの追加に失敗しました: {e}")
            return False

    def get_event_list(self, event_name, start_iso, end_iso):
        try:
            events_result = (
                self.service.events().list(
                    calendarId=self.calendar_id,
                    q=event_name,
                    timeMin=start_iso,
                    timeMax=end_iso,
                    singleEvents=True,
                    orderBy="startTime"
                ).execute()
            )
            
            events = events_result.get("items", [])
            logger.debug(
                f"{event_name}に該当する日時を全て取得しました: {events}"
            )

            return events
            
        except Exception as e:
            logger.error(
                f"イベント情報の取得中に予期せぬエラーが発生しました: {e}"
            )
            
def get_event_ids():
    from datetime_manager import DateTimeManager

    token_path = "../.config/cps/token_pickle"
    json_path = "../.config/cps/client_secret.json"
    sync_calendar = SyncGoogleCalendar(token_path, json_path)
    datetime_manager = DateTimeManager()
    
    event_name = "TA(Python プログラミング1)"
    input_date = "2025/10/20"
    start_moment = "10:30:00"
    end_moment = "12:00:00"

    start_iso = datetime_manager.convert_isoformat(input_date, start_moment)
    end_iso = datetime_manager.convert_isoformat(input_date, end_moment)

    event_id = sync_calendar.get_event_id(event_name, start_iso, end_iso)
    logger.info(
        f"{input_date}の{event_name}のID: {event_id}"
    )


def get_event_list():
    from datetime_manager import DateTimeManager
    from datetime import datetime

    token_path = "../.config/cps/token_pickle"
    json_path = "../.config/cps/client_secret.json"
    sync_calendar = SyncGoogleCalendar(token_path, json_path)
    datetime_manager = DateTimeManager()
    
    event_name = "TA(Python プログラミング1)"
    start_date = "2025/10/3"
    end_date = "2025/10/31"
    start_moment = "10:30:00"
    end_moment = "12:00:00"

    start_iso = datetime_manager.convert_isoformat(start_date, start_moment)
    end_iso = datetime_manager.convert_isoformat(end_date, end_moment)

    event_list = sync_calendar.get_event_list(event_name, start_iso, end_iso)

    event_dates = []
    for event in event_list:
        date = datetime.fromisoformat(
            event["start"]["dateTime"]
        )

        event_dates.append(
            date.strftime("%Y年%-m月%-d日")
        )
    logger.info(
        f"取得したイベントの予定日時: {event_dates}"
    )


if __name__ == "__main__":
    from setup_logging import setup_logging

    setup_logging("../.config/logging_config.yml")
    get_event_list()
    
