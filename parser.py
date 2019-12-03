import glob
import json


def parse():
    """
    Loads and prepares the *.json data for mapper
    """
    file_list = sorted(glob.glob('data/*.json'))
    for file in file_list:
        with open(file, 'r') as fp:
            content = json.load(fp)
            print(json.dumps(content))


if __name__ == '__main__':
    parse()
