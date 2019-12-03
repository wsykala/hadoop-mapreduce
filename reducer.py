from collections import defaultdict
import fileinput
from typing import Dict


def _parse_reduce_output(reduce_dict: Dict[str, Dict[str, int]]):
    for symbol, reduced_changes in reduce_dict.items():
        for change, count in reduced_changes.items():
            print(f'{symbol}\t{change}\t{count}')


def reducer():
    """
    Runs the reduce job.
    Input lines are passed as below:
    SYMBOL\tCHANGE\tCOUNT\n
    """
    all_symbol_dict = defaultdict(lambda: defaultdict(int))
    last_symbol = None
    symbol_dict = {}
    for line in fileinput.input():
        sanitized_line = line.strip()
        symbol, change, *_ = sanitized_line.split('\t')

        if not last_symbol or last_symbol != symbol:
            symbol_dict = all_symbol_dict[symbol]
        symbol_dict[change] += 1
        last_symbol = symbol

    _parse_reduce_output(all_symbol_dict)


if __name__ == '__main__':
    reducer()
