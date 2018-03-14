#!python3
# coding:utf-8
import os
import re
import msvcrt
from pattern3.en import lemma
import json
# number_of_all_words = 0
config = {
    'CONFIG_PATH': 'FAIDN.config',
    'MAIN_PATH': './',
    'NEW_WORDS_PATH': 'new.txt',
    'OLD_WORDS_PATH': 'old.txt',
    'ARTICLES_PATH': 'articles/',
    'NEW_WORDS_EACH_ARTICLE_PATH': 'new_words_of_each_article/',
}


def real_word(word):
    '''
    find the real word
    '''
    p_forword = re.compile('[a-z,A-Z,\',‘]')
    word = p_forword.findall(word)
    str = ''
    real_word = str.join(word)
    real_word = lemma(real_word)
    return real_word.lower()


def split_the_article(article):
    '''
    sklit the article
    '''
    sep = re.compile('[\r\n., ]')
    words = re.split(sep, article)
    filcts = (real_word(word) for word in words)
    set_of_words = set(filcts)
    return set_of_words


def read_new_words(path, known_words):
    '''
    read new words from article
    '''
    with open(path)as f_article:
        article = f_article.read()
    words = split_the_article(article)
    print('there are {} words in {}'.format(len(words), path))
    new_words = words - known_words
    num = len(new_words)
    if num == 0:
        print('No new word')
    elif num == 1:
        print('only 1 new word')
    else:
        print(str(num) + ' of them are new words')
    return new_words


def get_name(path):
    '''
    get the file Name
    '''
    try:
        names = os.listdir(path)
    except:
        os.mkdir(config['MAIN_PATH'] + config['ARTICLES_PATH'])
        names = os.listdir(path)
    return names


def read_known_words():
    '''
    load the word have known'''
    try:
        with open(config['MAIN_PATH'] + config['OLD_WORDS_PATH'])as f:
            all_the_words = f.read()
    except:
        print('\'' + config['MAIN_PATH'] +
              config['OLD_WORDS_PATH'] + '\' missing......')
        all_the_words = ""
    known_words = split_the_article(all_the_words)
    print(known_words)
    num = len(known_words)
    print('There are ' + str(num) + ' words I have known')
    return known_words


def my_input(output):
    '''
    input
    '''
    print(output)
    choise = ['1', '2']
    judge = msvcrt.getch().decode('utf-8')
    while judge == '\x00':
        judge = msvcrt.getch().decode('utf-8')
    if judge not in choise:
        print('Input error! Plz try again:')
        judge = my_input(output)
        return judge
    return judge


def learn(new_words, known_words):
    '''
    learn new words & build
    '''
    num = len(new_words)
    print('if you know the word print 1, else print 2')
    for word in new_words:
        num -= 1
        judge = my_input(word+'('+str(num)+' Left)\n')
        if judge == '1':
            known_words.add(word)
    return new_words - known_words, known_words


def write_each_new_words(name, new_words):
    '''
    write new words by each article
    '''
    try:
        os.makedirs(config['MAIN_PATH'] +
                    config['NEW_WORDS_EACH_ARTICLE_PATH'])
    except:
        pass
    try:
        with open(config['MAIN_PATH'] + config['NEW_WORDS_EACH_ARTICLE_PATH'] + name, 'w') as f_words:
            f_words.write('\n'.join(new_words))
    except:
        print('failed to creat file of \'' + config['MAIN_PATH'] +
              config['NEW_WORDS_EACH_ARTICLE_PATH'] + name + '\'')


def load_config():
    global config
    print('loading config from ' + config['CONFIG_PATH'] + '...')
    try:
        local_config = json.load(open(config['CONFIG_PATH']))
    except Exception as e:
        print('loading config failed\n writing default config to ' +
              config['MAIN_PATH'])
        json.dump(config, open(config['CONFIG_PATH'], 'w'))
        return
    try:
        for key in config:
            local_config[key]
    except Exception as e:
        print(str(e) + ' error')
        print('local config error, using default config')
        return
    config = local_config
    print('using local config')
    return


if __name__ == '__main__':
    '''
    main
    '''
    load_config()
    FLAG = 3
    while FLAG != 1 and FLAG != 2:
        print('print 1 to build model\nprint 2 to find model\n \
        here to get some help:https://zhuanlan.zhihu.com/p/25003457\n')
        FLAG = int(msvcrt.getch())
    NEM_WORDS_ALL = set()
    KNOWN_WORDS = read_known_words()
    PATH = config['MAIN_PATH'] + config['ARTICLES_PATH']
    FILE_NAMES = get_name(PATH)
    print(FILE_NAMES)
    for file_name in FILE_NAMES:
        print('opening' + file_name + '......')
        path_1 = PATH + '/' + file_name
        new_words = read_new_words(path_1, KNOWN_WORDS)
        if new_words:
            if FLAG == 1:
                new_words, KNOWN_WORDS = learn(new_words, KNOWN_WORDS)
                if new_words:
                    print('new words:')
                    print(new_words)
                    write_each_new_words(file_name, new_words)
                    NEM_WORDS_ALL = NEM_WORDS_ALL | set(new_words)
            else:
                NEM_WORDS_ALL = NEM_WORDS_ALL | set(new_words)
    with open(config['MAIN_PATH'] + config['OLD_WORDS_PATH'], 'w') as old:
        old.write('\n'.join(KNOWN_WORDS))
    with open(config['MAIN_PATH'] + config['OLD_WORDS_PATH'], 'w') as new:
        new.write('\n'.join(NEM_WORDS_ALL))
    # print(ord(msvcrt.getch()))
