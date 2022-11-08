import argparse
import concurrent.futures
import os
import pathlib
import subprocess
from colorama import Fore, Back, Style
from logging import DEBUG, basicConfig, getLogger

logger = getLogger(__name__)

def run(*, command: str, input_path: pathlib.Path, output_path: pathlib.Path, seed: int):
    logger.info(Fore.BLUE + 'running the command for seed %d...', seed)
    try:
        with open(input_path) as fh1:
            with open(output_path, 'w') as fh2:
                subprocess.check_call(command, stdin=fh1, stdout=fh2)
    except subprocess.SubprocessError:
        logger.exception(Fore.RED + 'failed for seed = %d', seed)


def main():
    option = argparse.ArgumentParser()
    option.add_argument('-f', '--file')
    option.add_argument('-t', '--testcases', type=int, default=50)
    option.add_argument('-p', '--parallel', type=int, default=1)
    args = option.parse_args()

    pathlib.Path('out').mkdir(exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.testcases) as executor:
        for i, seed in enumerate(0):
            input_path = pathlib.Path('in', '%04d.txt' % i)
            output_path = pathlib.Path('out', '%04d.txt' % i)
            executor.submit(run, file=args.file, input_path=input_path, output_path=output_path, seed=seed)

if __name__ == '__main__':
    main()