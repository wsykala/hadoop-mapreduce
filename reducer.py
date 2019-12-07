#!/usr/bin/python3

from collections import defaultdict
import fileinput
from typing import Dict


def _parse_reduce_output(reduce_dict: Dict[str, Dict[str, int]]):
    for symbol, reduced_changes in reduce_dict.items():
        for change, count in reduced_changes.items():
            print(f'{symbol}\t{change}\t{count}')


def _yield_symbol_dict(symbol: str, symbol_dict: dict):
    if not symbol:
        return
    for change, count in symbol_dict.items():
        print(f'{symbol}\t{change}\t{count}')


def reducer():
    """
    Runs the reduce job.
    Input lines are passed as below:
    SYMBOL\tCHANGE\tCOUNT\n
    """
    last_symbol = None
    symbol_dict = defaultdict(int)
    for line in fileinput.input():
        sanitized_line = line.strip()
        symbol, change, *_ = sanitized_line.split('\t')
        if not last_symbol or last_symbol != symbol:
            _yield_symbol_dict(last_symbol, symbol_dict)
            symbol_dict = defaultdict(int)
        symbol_dict[change] += 1
        last_symbol = symbol
    _yield_symbol_dict(last_symbol, symbol_dict)


if __name__ == '__main__':
    reducer()
