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
logger = logging.getLogger('FAIDN')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--mode', '-m', help='work mode\n 1 for build mode \n 2 for find mode \n default None', default=None)
    parser.add_argument(
        '--config', help='use local config', dest='config', default=True, action='store_true')
    parser.add_argument('--no-config', help='not use local config',
                        dest='config', action='store_false')
    args = parser.parse_args()
    CONFIG = safe_IO.load_json('./FAIDN.config')
    FLAG = safe_IO.check_flag(args.mode)
    safe_IO.check_output_file(CONFIG['MAIN_PATH'] + CONFIG['NEW_WORDS_PATH'])
    NEM_WORDS_ALL = set()
    FILE_NAMES = os.listdir(CONFIG['MAIN_PATH'] + CONFIG['ARTICLES_PATH'])
    NEW_WORDS_EACH_ARTICLE_PATH = CONFIG['MAIN_PATH'] + CONFIG['NEW_WORDS_EACH_ARTICLE_PATH']
    safe_IO.try_make_dir(CONFIG['MAIN_PATH'] + CONFIG['OLD_ARTICLES_PATH'])
    for file in FILE_NAMES:
        path = CONFIG['MAIN_PATH'] + CONFIG['ARTICLES_PATH'] + file
        article = Article(CONFIG,path)
        if FLAG==1:
            new_words, KNOWN_WORDS = article.learn()
            if new_words:
                logger.info('new words:')
                logger.info(new_words)
                safe_IO.write_each_new_words(NEW_WORDS_EACH_ARTICLE_PATH,file, new_words)
                NEM_WORDS_ALL = NEM_WORDS_ALL | set(new_words)
        else:
            new_words = article.new_words
            KNOWN_WORDS = article.known_words
            NEM_WORDS_ALL = NEM_WORDS_ALL | set(new_words)
            safe_IO.write_each_new_words(NEW_WORDS_EACH_ARTICLE_PATH, file, new_words)
        safe_IO.mv_file(path, CONFIG['MAIN_PATH'] + CONFIG['OLD_ARTICLES_PATH'])
        with open(CONFIG['MAIN_PATH'] + CONFIG['OLD_WORDS_PATH'], 'w') as old:
            old.write('\n'.join(KNOWN_WORDS))
        with open(CONFIG['MAIN_PATH'] + CONFIG['NEW_WORDS_PATH'], 'a') as new:
            new.write('\n'.join(NEM_WORDS_ALL))

if __name__ == '__main__':
    main()
