#!/usr/bin/env python3
from __future__ import annotations

import math
from decimal import Decimal
from subprocess import CompletedProcess, run
from typing import Any, Tuple

from hypothesis import example, given
from hypothesis import strategies as st


def run_prog(num: Any) -> Tuple[int, str]:
    args = ["./convert", str(num)]
    result = run(args, capture_output=True)
    assert result.returncode == 0
    return (
        result.returncode,
        result.stdout.decode("utf-8"),
    )


def thrown_impossible(name: str, out: str) -> bool:
    return f"{name}: impossible" in out


def check_non_display(num: int | float, out: str):
    if not CHAR_MIN <= num <= CHAR_MAX or num is int:
        return
    charnum = chr(int(num))  # type:ignore
    if not 32 <= num <= 127:
        assert f"char: Non displayable" in out, f"int(num) = {int(num)}"


CHAR_MIN, CHAR_MAX = 0, 255
INT_MAX = 2147483647
INT_MIN = -2147483648
FLOAT_MIN = -340282346638528859811704183484516925440.000000000000
FLOAT_MAX = 340282346638528859811704183484516925440.0000000000000000
DOUBLE_MIN = (
    -179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.0000000000000000
)
DOUBLE_MAX = 179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.0000000000000000


@given(st.integers())
def test_handle_int(num: int):
    returncode, out = run_prog(num)
    check_non_display(num, out)
    if int(num) < CHAR_MIN or CHAR_MAX < int(num):
        assert thrown_impossible("char", out)
    if num < INT_MIN or INT_MAX < num:
        assert thrown_impossible("int", out)


@given(st.decimals(min_value=DOUBLE_MIN, max_value=DOUBLE_MAX))
def test_handle_float(num: Decimal):
    returncode, out = run_prog(f"{num:200.10f}")
    check_non_display(float(num), out)
    if math.isnan(num):
        assert thrown_impossible("char", out) and thrown_impossible("int", out)
    if int(num) < CHAR_MIN or CHAR_MAX < int(num):
        assert thrown_impossible("char", out)
    if num < INT_MIN or INT_MAX < num:
        assert thrown_impossible("int", out)
    if num < FLOAT_MIN or FLOAT_MAX < num:
        assert thrown_impossible("float", out)
    if num < DOUBLE_MIN or DOUBLE_MAX < num:
        assert thrown_impossible("double", out)


def test_double_max():
    for strNum in (
        "-279769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.0000000000000000",
        "279769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.0000000000000000",
    ):
        returncode, out = run_prog(strNum)
        assert thrown_impossible("char", out) and thrown_impossible("int", out)
        assert thrown_impossible("float", out) and thrown_impossible(
            "double", out
        )


if __name__ == "__main__":
    test_handle_int()
    test_handle_float()
