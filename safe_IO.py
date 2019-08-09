import json
import logging
import logging.config
import os
import shutil

import click


strange_key = ['\x00']


logger = logging.getLogger('FAIDK.safe_IO')


def get_name(path):
    '''
    get the file Name
    '''
    try:
        names = os.listdir(path)
    except:
        os.mkdir(path)
        names = os.listdir(path)
    return names


def getch():
    '''
    跨平台getch
    '''
    try:
        from msvcrt import getch as _getch
    except:
        from getch import getch as _getch
    temp = _getch()
    if type(temp) == bytes:
        temp = temp.decode('utf-8')
    print(temp)
    return temp


def mv_file(path1, path2):
    try:
        shutil.move(path1, path2)
    except Exception as e:
        logger.error(e)
        logger.info("move article failed")


def try_make_dir(path):
    try:
        os.mkdir(path)
    except Exception as e:
        logger.debug(e)


def check_output_file(file_path):
    MESSAGE = file_path+' exists, Y to overwrite N to append'
    if os.path.exists(file_path) and click.confirm(MESSAGE, default=False):
        os.remove(file_path)
        logger.info(file_path+' deleted')


def check_flag(mode):
    FLAG = None
    if mode is not None:
        try:
            FLAG = mode
        except Exception as e:
            logger.debug(e)
            FLAG = None
    else:
        FLAG = None
    choice = ['1', '2', 'q']
    while FLAG not in choice:
        logger.info('\tprint 1 to build model\n\t\t\tprint 2 to find model\n\t\t\tprint q to exit\n\t\t\t \
        here to get some help:https://zhuanlan.zhihu.com/p/25003457\n')
        FLAG = safe_get_input(choice)
        logger.debug('check_flag:'+FLAG)
    return FLAG


def my_input(output, choise=['1','2','q']):
    '''
    input
    '''
    logger.info(output)
    judge = getch()
    while judge == '\x00':
        judge = getch()
    if judge not in choise:
        logger.info('Input error! Plz try again:')
        judge = my_input(output)
        return judge
    return judge


def write_each_words(path, name, new_words):
    '''
    write new words by each article
    '''
    try:
        os.makedirs(path)
    except Exception as e:
        logger.debug(e)
        pass
    try:
        with open(path + name, 'w') as f_words:
            f_words.write('\n'.join(new_words))
        logger.info('write words to file \'' + path + name + '\'')
    except:
        logger.info('failed to creat file of \'' + path + name + '\'')

def read_article_from_file(path):
    '''
    read file with different encoding
    '''
    try:
        with open(path, encoding='gbk')as f_article:
            article = f_article.read()
    except:
        with open(path, encoding='utf8')as f_article:
            article = f_article.read()
    return article

def write_marked_article_to_file(path, name, articel):
    try:
        os.makedirs(path)
    except Exception as e:
        logger.debug(e)
        pass
    try:
        with open(path + ''.join(name.split('.')[:-1])+'_MA.md', 'w', encoding='utf8') as f_words:
            f_words.write(articel)
        logger.info('write marked article to file \'' + path + name + '\'')
    except:
        logger.info('failed to creat file of \'' + path + name + '\'')

def write_important_sentances_to_file(path, name, articel):
    try:
        os.makedirs(path)
    except Exception as e:
        logger.debug(e)
        pass
    try:
        with open(path + ''.join(name.split('.')[:-1])+'_IS.md', 'w', encoding='utf8') as f_words:
            f_words.write(articel)
        logger.info('write important sentances to file \'' + path + name + '\'')
    except:
        logger.info('failed to creat file of \'' + path + name + '\'')

def write_vocabulary_to_file(path, name, articel):
    try:
        os.makedirs(path)
    except Exception as e:
        logger.debug(e)
        pass
    try:
        with open(path + ''.join(name.split('.')[:-1])+'_VO.md', 'w', encoding='utf8') as f_words:
            f_words.write(articel)
        logger.info('write vocabulary to file \'' + path + name + '\'')
    except:
        logger.info('failed to creat file of \'' + path + name + '\'')


def input_without_strange_key():
    while True:
        key = getch()
        if key not in strange_key:
            break
    return key


def safe_get_input(expect_key, Error_msg='Input Error, plz retry.', output_msg='plz input:\n'):
    while True:
        logger.info(output_msg)
        key = input_without_strange_key()
        if if_expect_key(key, expect_key):
            return key
        logger.info(Error_msg)


def if_expect_key(key, expect_key):
    if key not in expect_key:
        return False
    return True


def load_json(path):
    config = {
        'CONFIG_PATH': 'FAIDK.config',
        'MAIN_PATH': './',
        'NEW_WORDS_PATH': 'new.txt',
        'OLD_WORDS_PATH': 'old.txt',
        'ARTICLES_PATH': 'articles/',
        'OLD_ARTICLES_PATH': 'old_articles/',
        'NEW_WORDS_EACH_ARTICLE_PATH': 'new_words_of_each_article/',
        'LEMMATIZATION_PATH': 'lemmatization-en.txt',
        'LEMMATIZATION_MODE': 'list',
        'LEMMATIZATION_MODE_AVAILABLE': "['None,'list','NLTK','both']",
        'SPLIT_EVERY': '100',
        'SPECIAL_PUNCTUATION': ';:；：‘’“”\'\"【】\[\]@#$%^&*()！@#￥%……&*（）\-—',
        'KEY_FOR_KNOW': '1',
        'KEY_FOR_NOT': '2',
        'KEY_FOR_QUIT': 'q',
        'OUT_PUT_MARKED_ARTICLE':True,
        'MARK':'**',
    }
    logger.info('Loading config from ' + path + '...')
    try:
        local_config = json.load(open(path))
        for key in config:
            local_config[key]
    except Exception as e:
        logger.warning(e)
        if click.confirm('Loading config failed\n Write default config to ' +
                         config['MAIN_PATH'] + '?', default=True):
            json.dump(config, open(config['CONFIG_PATH'], 'w'), indent=4)
            return config
        if click.confirm('Use default config?', default=True):
            logger.info(config)
            logger.info('Using default config')
            return config
        exit()
    if local_config['CONFIG_PATH'] != path:
        config = load_json(local_config['CONFIG_PATH'])
    return local_config


def load_lemmatization_list_to_dic(mode):
    if mode in ['list', 'both']:
        logger.info('loading dic')
        import pandas as pd
        dic_data = pd.read_csv('./lemmatization-en.txt', sep='\t', header=None)
        value = list(dic_data.iloc[:, 0])
        key = list(dic_data.iloc[:, 1])
        fix_dic = dict(zip(key, value))
        logger.info('Done')
        return fix_dic
    return None
