import re

import IO


class Article(object):
    def __init__(self, config, path):
        self.config = config
        # self.config = IO.load_json(self.config[CONFIG_PATH])
        self.file_path = path
        OLD_WORDS_PATH = self.config['MAIN_PATH'] + self.config['OLD_WORDS_PATH']
        self.old_words = self.read_article(OLD_WORDS_PATH)
        self.article = self.read_article()
        self.words = self.split_the_article(self.article,self.file_path)
        self.new_words = self.read_new_words()

    def read_known_words(self,path):
        '''
        load the word have known
        '''
        try:
            with open(path)as f:
                all_the_words = f.read()
        except:
            print('\'' + path + '\' missing......')
            all_the_words = ""
        known_words = self.split_the_article(all_the_words,self.config['OLD_WORDS_PATH'])
        num = len(known_words)
        print('There are {} words in {}'.format(str(num),self.config['OLD_WORDS_PATH']))
        return known_words

    def read_article(self):
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

    def real_word(self, word):
        '''
        find the real word
        '''
        p_forword = re.compile('[a-z,A-Z,\',‘]')
        word = p_forword.findall(word)
        real_word = ''.join(word)
        return real_word.lower()

    def split_the_article(self,Article,name=None):
        '''
        split the article
        '''
        sep = re.compile('[\r\n., ]')
        words = re.split(sep, Article)
        filcts = (self.real_word(word) for word in words)
        set_of_words = set(filcts)
        if name==None:
            pass
        else:
            print('there are {} words in {}'.format(len(set_of_words), name))
        return set_of_words

    def read_new_words(self):
        '''
        read new words from article
        '''
        new_words = self.words - self.old_words
        num = len(new_words)
        if num == 0:
            print('No new word')
        elif num == 1:
            print('only 1 new word')
        else:
            print(str(num) + ' new words')
        return new_words

    def learn(self):
        '''
        learn new words & build
        '''
        num = len(new_words)
        print('if you know the word print 1, else print 2')
        for word in self.new_words:
            num -= 1
            judge = my_input(word+'('+str(num)+' Left)\n')
            if judge == '1':
                known_words.add(word)
        return self.new_words - self.known_words, self.known_words