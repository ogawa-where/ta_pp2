#!/usr/bin/env python3
#
# read_yml.py
#
# [概要]
# YAMLファイルを読み込んで，
# 設定情報を辞書型で返すプログラム．
# ＊loggingの設定で使用．
#

import yaml


def read_yml(yml_path: str):
    '''
    [概要]
    YAMLファイルを読み込んで，ファイル内のデータを辞書型で返す関数．

    Arg:
        yml_path (str): YAMLファイルのパス．

    Return:
        config (dict): 設定情報が書き込まれた辞書型データ．
    '''
    try:
        with open(yml_path, "rt") as yf:
            config = yaml.safe_load(yf.read())

        return config

    except FileNotFoundError as e:
        return None
