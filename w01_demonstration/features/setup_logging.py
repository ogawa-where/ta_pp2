#!/usr/bin/env python3
#
# setup_logging.py
#
# [概要]
# アプリケーションで使用している
# loggingモジュールに設定を適用させるための
# Pythonスクリプト．
#

#from read_yml import read_yml
from features.read_yml import read_yml

import logging
from logging import getLogger, basicConfig
from logging.config import dictConfig

from pathlib import Path


def setup_logging(config_path: str):
    '''
    [概要]
    read_ymlメソッドを呼び出して，取得した設定情報を適用するための関数．

    Arg:
        config_path (str): loggingの設定情報が書き込まれたYAMLファイル．
    '''
    config_file = Path(config_path)

    if config_file.exists():
        try:
            config = read_yml(config_file)

            dictConfig(config)
            getLogger(__name__).info(
                "Logging setup complete from YAML."
            )

        except Exception as e:
            basicConfig(level=logging.INFO)
            getLogger(__name__).error(
                f"Failed to read logging config from {config_path}: {e}"
            )
            getLogger(__name__).warning(
                "Using basicConfig as a fallback."
            )

    else:
        basicConfig(level=logging.INFO)
        getLogger(__name__).warning(
            f"Logging config file not found at {config_path}. Using basic."
        )
