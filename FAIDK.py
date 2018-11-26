import argparse
import logging
import os
import time

import click

import safe_IO
from Article import Article

try:
    os.mkdir('./log/')
except Exception as e:
    pass
logging.config.fileConfig('./logging.config')
logger = logging.getLogger('FAIDK')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--mode', '-m', help='work mode\n 1 for build mode \n 2 for find mode \n default None', default=None)
    parser.add_argument(
        '--config', help='use local config', dest='config', default=True, action='store_true')
    parser.add_argument('--no-config', help='not use local config',
                        dest='config', action='store_false')
    args = parser.parse_args()
    CONFIG = safe_IO.load_json('./FAIDK.config')
    FLAG = safe_IO.check_flag(args.mode)
    if FLAG == 'q':
        logger.info('user exit')
        return
    safe_IO.check_output_file(CONFIG['MAIN_PATH'] + CONFIG['NEW_WORDS_PATH'])
    NEM_WORDS_ALL = set()
    FILE_NAMES = safe_IO.get_name(
        CONFIG['MAIN_PATH'] + CONFIG['ARTICLES_PATH'])
    safe_IO.try_make_dir(CONFIG['MAIN_PATH'] + CONFIG['OLD_ARTICLES_PATH'])
    for file in FILE_NAMES:
        article = Article(CONFIG, file, FLAG)


if __name__ == '__main__':
    main()
