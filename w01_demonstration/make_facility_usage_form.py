#!/usr/bin/env python3
#
# make_facility_usage_form.py
# 
# [概要]
# featuresディレクトリに配置した
# datetime_managerとdocx_editorのクラスを呼び出して，
# inputディレクトリ内のfacility_use_form.docx(申請書)を
# 複製して適切に編集をするプログラム．
#

from features.datetime_manager import DateTimeManager
from features.docx_editor import DocxEditor

from datetime import datetime
from logging import getLogger
import os

logger = getLogger(__name__)


class MakeFacilityUsageForm:
    def __init__(self, input_form: str, output_form):
        self.docx_editor = DocxEditor(input_form, output_form)
        self.datetime_manager = DateTimeManager()

    def _make_date_dict(self, input_date=datetime.today()) -> dict:
        '''
        [概要]
        申請書に記載する，申請日を記録した辞書型を定義して返す関数．

        Arg:
            input_date: デフォルトはプログラムを実行した当日．
            ＊datetime型やstr型で入力することも可能．

        Return:
            dict: 和暦と月日を記録した辞書．
        '''
        logger.info("--- 申請日を記録した辞書型を定義 ---")
        return {
            "wareki":self.datetime_manager.convert_wareki(
                input_date,
                option="%-e"
            ),
            "mm": input_date.strftime("%-m"),
            "DD": input_date.strftime("%-d")
        }

    def _make_applicant_dict(
            self,
            department: str,
            student_number: str,
            student_name: str,
            group_name: str = " ",
            teacher_name: str = " ",
            purpose_of_use: str = "筋トレ",
            total_num: str = "1"
    ) -> dict:
        '''
        [概要]
        申請書に記載する，申請者本人の情報や団体情報，使用目的，合計人数を
        記録した辞書型を定義して返す関数．

        Args: 
            department: 学科(専攻)名
            student_number: 学籍番号
            student_name: 申請者(代表者)氏名
            group_name: 団体(部活・サークル)名．デフォルトはなし．
            teacher_name: 団体の場合，顧問の教員名を記載する．デフォルトはなし
            purpose_of_use: 使用目的．デフォルトは"筋トレ"
            total_num: 使用予定人数．デフォルトは"1人"

        Return:
            dict: 申請者に関する情報を記録した辞書．
        '''
        logger.info("--- 申請者情報を記録した辞書型を定義 ---")
        return {
            "department": department,
            "student_number": student_number,
            "student_name": student_name,
            "group_name": group_name,
            "teacher_name": teacher_name,
            "purpose_of_use": purpose_of_use,
            "total_num": total_num
        }

    def _make_usage_time_dict(
            self,
            a_or_p: str,
            sh: str,
            sm: str,
            eh: str,
            em: str
    ) -> dict:
        '''
        [概要]
        申請書に記載する，使用予定時間を記録した辞書型を定義する関数．

        Args: 
            a_or_p: 午前もしくは午後
            sh: 使用開始予定時間(時)
            sm: 使用終了予定時間(分)
            eh: 使用開始予定時間(時)
            em: 使用終了予定時間(分)

        Return:
            dict: 使用予定時間を記録した辞書
        '''
        logger.info("--- 使用時間を記録した辞書型を定義 ---")
        return {
            "A_or_P": a_or_p,
            "sH": sh,
            "sM": sm,
            "eH": eh,
            "eM": em
        }

    def make_placeholders(
            self,
            department: str,
            student_number: str,
            student_name: str,
            a_or_p: str,
            sh: str,
            sm: str,
            eh: str,
            em: str,
            group_name: str = " ",
            teacher_name: str = " ",
            purpose_of_use: str = "筋トレ",
            total_num: str = "1",
    ) -> dict:
        '''
        [概要]
        他関数で作成した辞書を呼び出して，連結するための関数．

        Args: 
            ＊割愛(他メソッド実行時に使用する引数群)

        Return:
            dict: 3つの辞書を連結した辞書データ
        '''
        date_dict = self._make_date_dict()
        applicant_dict = self._make_applicant_dict(
            department,
            student_number,
            student_name,
            group_name,
            teacher_name,
            purpose_of_use,
            total_num,
        )
        usage_time_dict = self._make_usage_time_dict(
            a_or_p, sh, sm, eh, em
        )

        logger.info("--- 全ての辞書を連結してプレースホルダーを定義 ---")
        return date_dict | applicant_dict | usage_time_dict

    def form_maker(self, placeholders, output_docx) -> None:
        '''
        [概要]
        秋田県立大学本荘キャンパスにて，体育館やトレーニングルームといった
        施設を利用する際に必要な申請書の書式を作成して保存するための関数．
    
        Args:
            placeholders: replace_paragraph_text()を動かすために使用する引数．
        '''
        paragraphs = self.docx_editor.read_cell_paragraphs()
    
        for paragraph in paragraphs:
            self.docx_editor.replace_paragraph_text(paragraph, placeholders)
        
        self.docx_editor.docx.save(output_docx)
        logger.info("--- プレースホルダーを参照してテキスト情報を置換完了 ---")


if __name__ == "__main__":
    "--- 手動テスト ---"
    from features.setup_logging import setup_logging
    
    setup_logging("./.config/logging_config.yml")

    logger.debug("=== MakeFacilityUsageForm 手動テスト開始 ===")
    
    os.makedirs(
        "output", exist_ok=True
    )
    
    input_docx = "./input/facility_use_form.docx"
    output_docx = "./output/output.docx"

    department = "総合システム工学専攻"
    student_number = "M26D003"
    student_name = "吉田 快"
    a_or_p = "午後"
    sh = "19"
    sm = "00"
    eh = "20"
    em = "30"
    
    make_facility_usage_form = MakeFacilityUsageForm(
        input_docx,
        output_docx
    )
    placeholders = make_facility_usage_form.make_placeholders(
        department,
        student_number,
        student_name,
        a_or_p, sh, sm, eh, em,
        total_num = "1"
    )
    make_facility_usage_form.form_maker(placeholders, output_docx)
    logger.debug("=== MakeFacilityUsageForm 手動テスト終了 ===")
