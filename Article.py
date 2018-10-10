import logging
import re

from nltk.stem import WordNetLemmatizer

from safe_IO import *

logger = logging.getLogger('FAIDN.Article')

class Article(object):
    def __init__(self, config, path):
        self.config = config
        # self.config = IO.load_json(self.config[CONFIG_PATH])
        self.file_path = path
        self.fix_dic = load_lemmatization_list_to_dic(self.config['LEMMATIZATION_MODE'])
        OLD_WORDS_PATH = self.config['MAIN_PATH'] + self.config['OLD_WORDS_PATH']
        self.known_words = self.split_the_article(self.read_old_words(OLD_WORDS_PATH))
        self.article = read_article_from_file(self.file_path)
        self.words = self.split_the_article(self.article,self.file_path)
        self.new_words = self.read_new_words()
        

    def read_old_words(self,path):
        try:
            return read_article_from_file(path)
        except:
            logger.info('missing ' + path)
            return ''

    def real_word(self, word):
        '''
        find the real word
        '''
        p_forword = re.compile('[a-z,A-Z,\',‘]')
        word = p_forword.findall(word)
        real_word = ''.join(word).lower()
        if self.config['LEMMATIZATION_MODE'] in ['list','both']:
            try:
                real_word = self.fix_dic[real_word]
            except Exception as e:
                logger.debug(e)
                pass
        if self.config['LEMMATIZATION_MODE'] in ['NLTK','both']:
            wordnet_lemmatizer = WordNetLemmatizer()
            real_word = wordnet_lemmatizer.lemmatize(real_word)
        return real_word

    def split_the_article(self, Article,name=None):
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
            logger.info('there are {} words in {}'.format(len(set_of_words), name))
        return set_of_words

    def read_known_words(self,path):
        '''
        load the word have known
        '''
        try:
            with open(path)as f:
                all_the_words = f.read()
        except:
            logger.info('\'' + path + '\' missing......')
            all_the_words = ""
        known_words = split_the_article(all_the_words,self.config['OLD_WORDS_PATH'])
        num = len(known_words)
        logger.info('There are {} words in {}'.format(str(num),self.config['OLD_WORDS_PATH']))
        return known_words

    def read_new_words(self):
        '''
        read new words from article
        '''
        new_words = self.words - self.known_words
        num = len(new_words)
        if num == 0:
            logger.info('No new word')
        elif num == 1:
            logger.info('only 1 new word')
        else:
            logger.info(str(num) + ' new words')
        return new_words

    def learn(self):
        '''
        learn new words & build
        '''
        num = len(self.new_words)
        logger.info('if you know the word 1, else print 2')
        for word in self.new_words:
            num -= 1
            judge = my_input(word+'('+str(num)+' Left)\n')
            if judge == '1':
                self.known_words.add(word)
        return self.new_words - self.known_words, self.known_words
