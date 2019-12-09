import glob
import json
import os

from tqdm import tqdm


path = os.path.dirname(os.path.abspath(__file__))


def parse():
    """
    Loads and prepares the *.json data for mapper
    """
    print('Parsing data')
    file_list = sorted(glob.glob(f'{path}/data/*.json'))
    with open(os.path.join(path, 'parse.txt'), 'w') as parsed_file:
        for file in tqdm(file_list):
            with open(file, 'r') as fp:
                content = json.load(fp)
                parsed_file.write(f'{json.dumps(content)}\n')


if __name__ == '__main__':
    parse()
