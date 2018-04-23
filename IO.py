import json
import msvcrt

import click


class IO(object):
    def __init__(self):
        self.config = {
            'CONFIG_PATH': 'FAIDN.config',
            'MAIN_PATH': './',
            'NEW_WORDS_PATH': 'new.txt',
            'OLD_WORDS_PATH': 'old.txt',
            'ARTICLES_PATH': 'articles/',
            'NEW_WORDS_EACH_ARTICLE_PATH': 'new_words_of_each_article/',
        }
        self.strange_key = ['\x00']

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
        if type(expect_key) is list:
            if key not in  expect_key:
                return False
        else:
            if key != expect_key:
                return False
        return True

    def load_json(self):
        print('loading config from ' + self.config['CONFIG_PATH'] + '...')
        try:
            local_config = json.load(open(self.config['CONFIG_PATH']))
        except Exception as e:
            if click.confirm('loading config failed\n write default config to ' +
                self.config['MAIN_PATH'] + '?',default=True):
                json.dump(self.config, open(self.config['CONFIG_PATH'], 'w'), indent=4)
            else:
                exit()
            return
        try:
            for key in self.config:
                local_config[key]
        except Exception as e:
            print(str(e) + ' error')
            print('local config error, using default config')
            return
        self.config = local_config
        print('using local config')
        return
