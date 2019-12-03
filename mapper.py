import fileinput
import json
from typing import List


def _calculate_change(current: float, previous: float) -> float:
    try:
        return round((current - previous) / previous * 100, 2)
    except ZeroDivisionError:
        return 0.0


def _map_entry(symbol: str, data: List[dict]):
    previous = data[0]['close']
    for single in data[1:]:
        current = single['close']
        change = _calculate_change(current, previous)
        previous = current
        print(f'{symbol}\t{change}\t1')


def mapper():
    """
    Maps the historical prices and calculates the change for each company
    The input lines MUST be in a format of json dict (as specified in financial API)
    """
    for line in fileinput.input():
        content = json.loads(line.strip())
        entry_content = content.get('historicalStockList', [content])
        for entry in entry_content:
            entry_name = entry['symbol']
            entry_data = entry['historical']
            _map_entry(entry_name, entry_data)


if __name__ == '__main__':
    mapper()
