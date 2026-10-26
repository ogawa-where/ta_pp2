#!/usr/bin/env python3
#
# mcdonalds_order.py
# 
# [概要]
# ハンバーガーチェーン店であるマクドナルドにて
# 店頭での注文シーンをざっくり再現した
# プログラム．
#

import pyinputplus as pyip
import re

# ハンバーガー名と単品価格を辞書型で定義
BURGER_PRICES = {
    "ビッグマック": 480,
    "炙り醤油風 ダブル肉厚ビーフ": 580,
    "炙り醤油風 たまごベーコン肉厚ビーフ": 570,
    "ダブルチーズバーガー": 450,
    "チキチー": 250
}

# サイドメニュー名と単品価格を辞書型で定義
SIDEMENU_PRICES = {
    "マックフライポテト(M)": 330,
    "チキンマックナゲット(5P)": 290,
    "サイドサラダ": 350,
    "えだまめコーン": 300,
    "シャカチキ": 220
}

# ドリンク名と単品価格を辞書型で定義
DRINK_PRICES = {
    "コカ・コーラ(M)": 270,
    "スプライト(M)": 270,
    "ファンタ メロン(M)": 270,
    "爽健美茶": 270,
    "プレミアムローストコーヒー(M)": 180
}


def burger_order():
    '''
    [概要]
    ハンバーガーを数値で注文するための関数．
    実行されると，各ハンバーガーに数値が付与される．
    
    Return:
       burger (str): 入力された数値と紐づけられたハンバーガー名のテキスト
    '''
    burger = pyip.inputMenu(
        (
            "ビッグマック",
            "炙り醤油風 ダブル肉厚ビーフ",
            "炙り醤油風 たまごベーコン肉厚ビーフ",
            "ダブルチーズバーガー",
            "チキチー"
        ),
        prompt="お好みのバーガーを選択してください．\n",
        numbered=True
    )

    return burger


def sidemenu_order():
    '''
    [概要]
    サイドメニューを数値で注文するための関数．
    実行されると，各サイドメニューに数値が付与される．
    
    Return:
       sidemenu (str): 入力された数値と紐づけられたサイドメニューのテキスト
    '''
    sidemenu = pyip.inputMenu(
        (
            "マックフライポテト(M)",
            "チキンマックナゲット(5P)",
            "サイドサラダ",
            "えだまめコーン",
            "シャカチキ"
        ),
        prompt="サイドメニューを選択してください．\n",
        numbered=True
    )

    return sidemenu


def drink_order():
    '''
    [概要]
    ドリンクを数値で注文するための関数．
    実行されると，各ドリンクに数値が付与される．
    
    Return:
       drink (str): 入力された数値と紐づけられたドリンク名のテキスト
    '''
    drink = pyip.inputMenu(
        (
            "コカ・コーラ(M)",
            "スプライト(M)",
            "ファンタ メロン(M)",
            "爽健美茶",
            "プレミアムローストコーヒー(M)"
        ),
        prompt="お飲み物を選んでください．\n",
        numbered=True
    )

    return drink


def order_check():
    '''
    [概要]
    追加注文の有無を"はい"か"いいえ"で入力するための関数．
    
    Return:
       decision (str): "はい"もしくは"いいえ"というテキストデータ
    '''
    decision = pyip.inputYesNo(
        "ご注文は以上でよろしいでしょうか?('はい'/'いいえ')\n",
        yesVal="はい",
        noVal="いいえ"
    )

    return decision


def accountiong(total_price):
    '''
    [概要]
    お会計用の関数．
    5秒以内に支払いが完了しなければ取引がキャンセルされる．
    
    Arg:
        total_price (int): 注文されたメニューに応じた合計金額
    '''
    try:
        cash = pyip.inputInt(
            "5秒以内にお支払いください．\n",
            limit=3,
            timeout=5,
            blockRegexes=[(r"^0$", "0円では支払えません．")]
        )

        if cash < total_price:
            print("現金が足りません．取引をキャンセルします．")

        else:
            change = cash - total_price
            print(f"お支払いありがとうございます．お釣りは {change} 円です．")
            return change

    except pyip.RetryLimitException:
        print("3回の入力を超えました．取引をキャンセルします．")
        return 
        
    except pyip.TimeoutException:
        print("時間切れです．取引をキャンセルします．")
        return
    

def price_check():
    '''
    [概要]
    上で定義したすべての関数を連動させるための関数．
    ハンバーガー・サイドメニュー・ドリンクの注文内容に応じた
    合計金額を算出している．
    '''
    total_price = 0

    while True:
        burger = burger_order()
        total_price += BURGER_PRICES[burger]
    
        sidemenu = sidemenu_order()
        total_price += SIDEMENU_PRICES[sidemenu]
    
        drink = drink_order()
        total_price += DRINK_PRICES[drink]

        decision = order_check()
        if decision == "はい":
            break
        
    print("-" * 15)
    print(f"お会計は {total_price} 円となります．")

    accountiong(total_price)
    

if __name__ == "__main__":
    price_check()
