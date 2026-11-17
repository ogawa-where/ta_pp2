#!/usr/bin/env python3

from setup_logging import setup_logging
from logging import getLogger


setup_logging()
logger = getLogger(__name__)


logger.info("=== Python プログラミング2 デバッグの復習 ===")

while True:
    x = input("1つ目の整数を入力してください（終了: q）")
    if x == "q":
        break

    y = input("2つ目の整数を入力してください")
    op = input("演算子を入力してください（+, -, *, /）")

    try:
        a = int(x)
        b = int(y)

        assert op in ["+", "-", "*", "/"], "演算子が不正です"

        if op == "/" and b == 0:
            raise ZeroDivisionError("0 で割ることはできません")

        if op == "+":
            r = a + b

        elif op == "-":
            r = a - b

        elif op == "*":
            r = a * b

        else:
            r = a / b

    except ValueError:
        logger.error("入力は整数のみ有効です")

    except AssertionError as e:
        logger.error(e)

    except ZeroDivisionError as e:
        logger.error(e)

    else:
        logger.info(f"計算結果: {r}")
