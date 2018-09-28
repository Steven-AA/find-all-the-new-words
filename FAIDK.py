import argparse
import logging
import time
import os
from Article import Article
import safe_IO

# FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
# logging.basicConfig(format=FORMAT)
# logging_name = time.strftime('%Y-%m-%d-%H',time.localtime())
# file_handler = logging.FileHandler("{}.log".format(logging_name))  
# file_handler.setFormatter(formatter)  

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--mode', '-m', help='work mode\n 1 for build mode \n 2 for find mode \n default None', default=None)
    parser.add_argument(
        '--config', help='use local config', dest='config', default=True, action='store_true')
    parser.add_argument('--no-config', help='not use local config',
                        dest='config', action='store_false')
    args = parser.parse_args()
    CONFIG = {
            'CONFIG_PATH': 'FAIDN.config',
            'MAIN_PATH': './',
            'NEW_WORDS_PATH': 'new.txt',
            'OLD_WORDS_PATH': 'old.txt',
            'ARTICLES_PATH': 'articles/',
            'NEW_WORDS_EACH_ARTICLE_PATH': 'new_words_of_each_article/',
        }
    CONFIG = safe_IO.load_json(CONFIG['CONFIG_PATH'])
    FLAG = None
    if args.mode is not None:
        try:
            FLAG = int(args.mode)
        except Exception as e:
            print(e)
            FLAG = None
    else:
        FLAG = None
    while FLAG != 1 and FLAG != 2:
        print('print 1 to build model\nprint 2 to find model\n \
        here to get some help:https://zhuanlan.zhihu.com/p/25003457\n')
        FLAG = int(safe_IO.safe_get_input(['1','2']))
        # FLAG = int(msvcrt.getch())
    NEM_WORDS_ALL = set()
    FILE_NAMES = os.listdir(CONFIG['MAIN_PATH'] + CONFIG['ARTICLES_PATH'])
    for file in FILE_NAMES:
        path = CONFIG['MAIN_PATH'] + CONFIG['ARTICLES_PATH'] + file
        article = Article(CONFIG,path)
        if FLAG==1:
            new_words, KNOWN_WORDS = article.learn()
            if new_words:
                print('new words:')
                print(new_words)
                safe_IO.write_each_new_words(CONFIG['MAIN_PATH'] + CONFIG['NEW_WORDS_EACH_ARTICLE_PATH'],file, new_words)
                NEM_WORDS_ALL = NEM_WORDS_ALL | set(new_words)
        else:
            new_words = article.new_words
            KNOWN_WORDS = article.known_words
            NEM_WORDS_ALL = NEM_WORDS_ALL | set(new_words)
        with open(CONFIG['MAIN_PATH'] + CONFIG['OLD_WORDS_PATH'], 'w') as old:
            old.write('\n'.join(KNOWN_WORDS))
        with open(CONFIG['MAIN_PATH'] + CONFIG['NEW_WORDS_PATH'], 'w') as new:
            new.write('\n'.join(NEM_WORDS_ALL))

if __name__ == '__main__':
    main()
