import fileinput
import json
from typing import List


class StockEntry(object):
    def __init__(self, *, symbol: str):
        self.symbol = symbol
        self.date: List[str] = []
        self.close_price: List[float] = []
        self.__counter = 0

    def length(self):
        return len(self.close_price)

    def generate_changes(self):
        try:
            for i in range(len(self.close_price)):
                previous = self.close_price[i]
                current = self.close_price[i + 1]
                try:
                    result = round((current - previous) / previous * 100, 2)
                except ZeroDivisionError:
                    result = 0.0
                yield result
        except IndexError:
            return


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
            stock_entry = StockEntry(symbol=entry_name)
            for single in entry_data:
                stock_entry.close_price.append(single['close'])
                stock_entry.date.append(single['date'])
            for change in stock_entry.generate_changes():
                print(f'{stock_entry.symbol}\t{change}\t1')


if __name__ == '__main__':
    mapper()
