import json
import os
import pathlib
import time
from typing import List, Optional

import requests


_STOCK_LIST_URL = 'https://financialmodelingprep.com/api/v3/company/stock/list'
_API_URL_TEMPLATE = 'https://financialmodelingprep.com/api/v3/' \
                    'historical-price-full/{}?serietype=line'


def _fetch(url: str, **kwargs: dict) -> Optional[requests.Response]:
    response = requests.get(url, **kwargs)
    if response.ok:
        return response
    raise RuntimeError(f'[{response.status_code}] for [{url}]')


def _get_stock_list() -> List[str]:
    stock_list_response = _fetch(_STOCK_LIST_URL)
    symbols_json = stock_list_response.json().get('symbolsList', None)
    symbols_list = []
    if not symbols_json:
        return symbols_list

    symbols_list = list(
        filter(None, (entry.get('symbol', None) for entry in symbols_json))
    )
    return sorted(symbols_list)


def run():
    data_dir = 'data'
    pathlib.Path(data_dir).mkdir(parents=True, exist_ok=True)
    stock_list = _get_stock_list()
    for i in range(0, len(stock_list), 3):
        symbols = stock_list[i:i+3]
        url = _API_URL_TEMPLATE.format(','.join(symbols))
        file_name = '_'.join(symbols) + '.json'
        file_path = os.path.join(data_dir, file_name)
        if os.path.exists(file_path):
            continue
        print(f'Fetching {url}')
        response = _fetch(url)
        with open(file_path, 'w') as file:
            json.dump(response.json(), file, indent=4)
        time.sleep(0.25)


if __name__ == '__main__':
    run()
