import argparse
import os
import subprocess
import time
from typing import Tuple

from request import run as download
from parser import parse

_command = ['/usr/local/hadoop/bin/hadoop', 'jar',
            '/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.0.jar', '-file',
            '/mapreduce/mapper.py', '-mapper',
            'mapper.py', '-file', '/mapreduce/reducer.py',
            '-reducer', 'reducer.py']
_mkdir_command = ['/usr/local/hadoop/bin/hdfs', 'dfs', '-mkdir', '-p']
_put_command = ['/usr/local/hadoop/bin/hdfs', 'dfs', '-put']


def _parse_args():
    parser = argparse.ArgumentParser(description='Run mapreduce job')
    parser.add_argument('--input', required=True, type=str, help='Path to input file inside HDFS')
    parser.add_argument('--output', required=True, type=str,
                        help='HDFS output path (timestamp will be added at the end)')
    parser.add_argument('--download', default='True', type=str, help='Download files')
    return parser.parse_args()


def _download_data(download_flag: str):
    if download_flag.lower() == 'true':
        download()
    parse()

def _run_extend(cmd: list, arguments: list):
    if arguments:
        cmd.extend(arguments)
    subprocess.run(cmd)

def _prepare_hdfs(input_file: str, out_dir: str) -> Tuple[str, str]:
    timestamp = str(int(time.time()))
    hdfs_dir = os.path.join(out_dir, timestamp)
    hdfs_input_file = os.path.join(hdfs_dir, input_file.split('/')[-1])
    _run_extend(_mkdir_command, [hdfs_dir])
    _run_extend(_put_command, [input_file, hdfs_dir])
    return hdfs_input_file, os.path.join(hdfs_dir, 'out')


def run_map_reduce_job():
    args = _parse_args()
    _download_data(args.download)
    hdfs_in, hdfs_out =_prepare_hdfs(args.input, args.output)
    _run_extend(_command, ['-input', hdfs_in, '-output', hdfs_out])


if __name__ == '__main__':
    run_map_reduce_job()
