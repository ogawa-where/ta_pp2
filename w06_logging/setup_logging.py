#!/usr/bin/env python3
#
# setup_logging.py
# 
# [概要]
# loggingの設定を一括で完了させる
# プログラム．
# コンソールやログファイルへの出力様式を
# 定義している．
#

import logging
from logging import handlers

logger = logging.getLogger(__name__)


def setup_logging():
    '''
    [概要]
    logging全体の設定をおこなう関数．
    '''
    try:
        console_handler, file_handler = setup_handlers()
        setup_root_logger(console_handler, file_handler)

        logger.debug("loggingの設定が正常に完了しました．")
        logger.info("loggingの設定が正常に完了しました．")
#        logger.warning("警告: 設定ファイルが見つかりません．")
#        logger.error("エラー: データベースに接続できません．")
#        logger.critical("致命的エラー: アプリを強制終了します．")

    except Exception as e:
        logging.basicConfig(level=logging.ERROR)
        logger.error(
            f"logging設定中に予期せぬエラーが発生しました: {e}"
        )


def setup_formatters():
    '''
    [概要]
    CLI用のフォーマッタとログファイル用のフォーマッタを
    設定する関数．
    '''
    try:
        cli_formatter = logging.Formatter(
            fmt="%(levelname)-8s - %(name)s - %(message)s"
        )

        logfile_formatter = logging.Formatter(
            fmt="%(asctime)s - %(levelname)-8s - %(name)s - [%(funcName)s:%(lineno)d] - %(message)s"
        )

        return cli_formatter, logfile_formatter

    except Exception as e:
        logger.error(
            f"フォーマッタ設定中に予期せぬエラーが発生しました: {e}"
        )
        raise


def setup_handlers():
    '''
    [概要]
    CLIハンドラとログファイルハンドラを設定する関数．
    '''
    try:
        cli_formatter, logfile_formatter = setup_formatters()
    
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(cli_formatter)

        file_handler = handlers.RotatingFileHandler(
            filename="pp2_app.log",
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8"
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logfile_formatter)

        return console_handler, file_handler

    except Exception as e:
        logger.error(
            f"ハンドラ設定中に予期せぬエラーが発生しました: {e}"
        )
        raise


def setup_root_logger(console_handler, file_handler):
    '''
    [概要]
    ルートロガーを設定する関数．
    '''
    try:
        logging.basicConfig(
            level=logging.DEBUG,
            handlers=[
                console_handler,
                file_handler
            ]
        )

    except Exception as e:
        logger.error(
            f"ルートロガー設定中に予期せぬエラーが発生しました: {e}"
        )
        raise

    
if __name__ == "__main__":
    setup_logging()
