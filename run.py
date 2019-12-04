import argparse
import os
import subprocess
import time

_command = ['/usr/local/hadoop/bin/hadoop', 'jar',
            '/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.0.jar', '-file',
            '/mapreduce/mapper.py', '-mapper',
            'mapper.py', '-file', '/mapreduce/reducer.py',
            '-reducer', 'reducer.py']


def _parse_args():
    parser = argparse.ArgumentParser(description='Run mapreduce job')
    parser.add_argument('--input', required=True, help='Path to input file inside HDFS')
    parser.add_argument('--output', required=True, help='HDFS output path (timestamp will be added at the end)')
    return parser.parse_args()


def run_map_reduce_job():
    args = _parse_args()
    timestamp = str(int(time.time()))
    output = os.path.join(args.output, timestamp)
    _command.extend(['-input', args.input, '-output', output])
    subprocess.run(_command)


if __name__ == '__main__':
    run_map_reduce_job()
