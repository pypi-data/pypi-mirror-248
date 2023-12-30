from .fuzzy import *
import yaml
import argparse
import os
import warnings


def read_conf(path: str) -> dict:
    with open(path, 'r') as fh:
        data = yaml.safe_load(fh)

    return data

# cli app
def app() -> None:
    warnings.filterwarnings("ignore")
    ROOTDIR = os.path.dirname(os.path.abspath(__file__))
    conf = read_conf(os.path.join(ROOTDIR, 'conf.yml'))
    HZ, ROLL, TONES, RATE = conf['hz'], conf['roll'], conf['tones'], conf['rate']

    parser = argparse.ArgumentParser(
        prog="muffler"
    )

    file_or_dir = parser.add_mutually_exclusive_group(required=True)
    file_or_dir.add_argument('-f', '--file')
    file_or_dir.add_argument('-r', '--read-dir', dest='read_dir')
    parser.add_argument('-d', '--dest')
    params = parser.parse_args()


    # 1 file no overwrite
    if params.file and params.dest:
        fuzzify(params.file, dest=params.dest, _hz=HZ, _roll=ROLL, _tones=TONES, _rate=RATE)

    # 1 file overwrite
    elif params.file:
        fuzzify(params.file, _hz=HZ, _roll=ROLL, _tones=TONES, _rate=RATE)

    # 1 dir no overwrite
    elif params.read_dir and params.dest:
        fuzzify_all(params.read_dir, write_dir=params.dest, _hz=HZ, _roll=ROLL, _tones=TONES, _rate=RATE)

    # 1 dir overwrite
    else:
        fuzzify_all(params.read_dir, _hz=HZ, _roll=ROLL, _tones=TONES, _rate=RATE)
    


if __name__ == '__main__':
    app()
