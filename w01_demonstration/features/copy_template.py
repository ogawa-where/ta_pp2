#!/usr/bin/env python3
#
# copy_template.py
# 
# [概要]
#
#
#
#
#

import shutil
from logging import getLogger
import os

logger = getLogger(__name__)


def copy_template(input_path: str, output_path: str):
    '''
    [概要]
    標準モジュールであるshutilを使って，テンプレート書式を複製する関数．
    クラス呼び出し時の__init__で使われる．

    Args:
        input_docx (str): 複製用のテンプレート書式が配置されたパス．
        output_docx (str): 複製後の書式．クラス内の処理ではこちらを編集する
    '''
    try:
        shutil.copy(
            input_path, output_path
        )
        logger.info(
            f"テンプレートを複製しました: {input_path} -> {output_path}"
        )
        
    except FileNotFoundError:
        logger.error(
            f"コピー元の書式が見つかりません: {input_path}"
        )
        raise
    
    except PermissionError:
        logger.error(
            f"ファイルへのアクセス権限がありません: {output_path}"
        )
        raise
    
    except shutil.SameFileError:
        logger.error(
            f"コピー元とコピー先が同じファイルです: {input_path}"
        )
        raise
    
    except Exception as e:
        logger.exception(
            f"複製中に予期せぬエラーが発生しました: {e}"
        )
        raise
    

if __name__ == "__main__":
    "=== 手動テスト ==="
    from setup_logging import setup_logging

    setup_logging("../.config/logging_config.yml")

    logger.debug("=== copy_template 手動テスト開始 ===")
    os.makedirs(
        "output", exist_ok=True
    )
    input_path = "../input/ta_monthly_work_report.xlsx"
    output_path = "./output/output.xlsx"

    copy_template(input_path, output_path)

    logger.debug("=== copy_template 手動テスト終了 ===")
    
