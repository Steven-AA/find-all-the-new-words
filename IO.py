import json
import logging
import msvcrt

import click


class IO(object):
    def __init__(self):
        self.strange_key = ['\x00']

    # def get_name(self,path):
    #     '''
    #     get the file Name
    #     '''
    #     try:
    #         names = os.listdir(path)
    #     except:
    #         os.mkdir(config['MAIN_PATH'] + config['ARTICLES_PATH'])
    #         names = os.listdir(path)
    #     return names
    
    def read_known_words():
        '''
        load the word have known
        '''
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

    def read_article_from_file(self,path):
                '''
        read file with different encoding
        '''
        try:
            with open(self.file_path, encoding='gbk')as f_article:
                article = f_article.read()
        except:
            with open(self.file_path, encoding='utf8')as f_article:
                article = f_article.read()
        return article
    
    def input_without_strange_key(self):
        while True:
            key = msvcrt.getch().decode('utf-8')
            if key not in self.strange_key:
                break
        return key

    def safe_get_input(self, expect_key, Error_msg='Input Error, plz retry.', output_msg='plz input:\n'):
        while True:
            print(output_msg)
            key = self.input_without_strange_key()
            if self.if_expect_key(key, expect_key):
                return key
            print(Error_msg)

    def if_expect_key(self, key, expect_key):
        if key not in  expect_key:
                return False
        else:
            if key != expect_key:
                return False
        return True

    def load_json(self,path):
        config = {
            'CONFIG_PATH': 'FAIDN.config',
            'MAIN_PATH': './',
            'NEW_WORDS_PATH': 'new.txt',
            'OLD_WORDS_PATH': 'old.txt',
            'ARTICLES_PATH': 'articles/',
            'NEW_WORDS_EACH_ARTICLE_PATH': 'new_words_of_each_article/',
        }
        print('Loading config from ' + path + '...')
        try:
            local_config = json.load(open(path))
            for key in config:
                local_config[key]
            print('Using local config')
            return local_config
        except Exception as e:
            print(e)
            if click.confirm('Loading config failed\n Write default config to ' +
                config['MAIN_PATH'] + '?',default=True):
                json.dump(config, open(config['CONFIG_PATH'], 'w'), indent=4)
                return config
            if click.confirm('Use default config?', default=True):
                print(config)
                print('Using default config')
                return config
            exit()

