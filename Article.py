import logging
import re

from nltk.stem import WordNetLemmatizer
from nltk import tokenize

import safe_IO
from safe_IO import *

logger = logging.getLogger('FAIDK.Article')


class Article(object):
    def __init__(self, config, file, FLAG):
        self.name = file
        self.config = config
        self.mark = self.config["MARK"]
        self.file_path = config['MAIN_PATH'] + config['ARTICLES_PATH'] + file
        self.fix_dic = load_lemmatization_list_to_dic(
            self.config['LEMMATIZATION_MODE'])
        self.known_words = self.read_known_words()
        self.article = read_article_from_file(self.file_path)
        self.words = self.split_the_article(self.article, self.file_path)
        self.new_words = self.read_new_words()
        self.num = len(self.new_words)
        self.keys = self.load_keys()
        if FLAG == '1':
            self.learn()
        if FLAG=='2':
            self.finish()
        if self.config['OUT_PUT_MARKED_ARTICLE']:
            self.out_put_markded_article()
        self.out_put_important_sentences()
    
    def out_put_markded_article(self):
        self.pattern = re.compile(r"(\b"+r"\b|\b".join(self.new_words)+"\b)",flags=re.IGNORECASE)
        self.marked_article = re.sub(self.pattern,self.mark+r"\1"+self.mark,self.article)
        write_marked_article_to_file("./others/",self.name, self.marked_article)
    
    def out_put_important_sentences(self):
        sentences = tokenize.sent_tokenize(self.marked_article)
        i_sentences = [_ if self.pattern.search(_) else None for _ in sentences]
        write_important_sentances_to_file("./others/",self.name, "\n\n".join(list(filter(None,i_sentences))))



    def load_keys(self):
        f = self.config
        keys = [f['KEY_FOR_KNOW'], f['KEY_FOR_NOT'], f['KEY_FOR_QUIT']]
        logger.debug(keys)
        return keys

    def read_old_words(self, path):
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
        word_s = p_forword.findall(word)
        real_word = ''.join(word_s).lower()
        if self.config['LEMMATIZATION_MODE'] in ['list', 'both']:
            try:
                real_word = self.fix_dic[real_word]
            except Exception as e:
                logger.debug(e)
                pass
        if self.config['LEMMATIZATION_MODE'] in ['NLTK', 'both']:
            wordnet_lemmatizer = WordNetLemmatizer()
            real_word = wordnet_lemmatizer.lemmatize(real_word)
        logger.debug(word+'-->'+real_word)
        return real_word

    def read_known_words(self):
        '''
        load the word have known
        '''
        try:
            with open(self.config['MAIN_PATH'] + self.config['OLD_WORDS_PATH'])as f:
                all_the_words = f.read()
        except:
            logger.info('\'' + self.config['MAIN_PATH'] +
                        self.config['OLD_WORDS_PATH'] + '\' missing......')
            all_the_words = ""
        known_words = self.split_the_article(all_the_words)
        logger.info(known_words)
        num = len(known_words)
        logger.info('There are ' + str(num) + ' words I have known')
        return known_words

    def split_the_article(self, Article, name=None):
        '''
        split the article
        '''
        sep = re.compile('[ \r\n.,'+self.config['SPECIAL_PUNCTUATION']+' ]')
        logger.debug(sep)
        words = re.split(sep, Article)
        filcts = (self.real_word(word) for word in words)
        set_of_words = set(filcts)
        if name == None:
            pass
        else:
            logger.info('there are {} words in {}'.format(
                len(set_of_words), name))
            logger.debug(set_of_words)
        return set_of_words

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
        logger.info(new_words)
        return sorted(new_words)

    def learn(self):
        '''
        learn new words & build
        '''
        logger.info('if you know the word {}, else print {}'.format(self.config['KEY_FOR_KNOW'],self.config['KEY_FOR_NOT']))
        for word in self.new_words:
            judge = my_input(word+'('+str(self.num)+' Left)',self.keys)
            if judge == self.config['KEY_FOR_QUIT']:
                self.user_exit()
                return
            if judge == self.config['KEY_FOR_KNOW']:
                self.known_words.add(word)
            self.num -= 1
        self.new_words = sorted(set(self.new_words) - self.known_words)
        if self.new_words:
            logger.info('new words ({}):'.format(len(self.new_words)))
            logger.info(self.new_words)
        self.finish()

    def user_exit(self):
        write_each_words(
            self.config['ARTICLES_PATH'], 'l_'+self.name, list(self.new_words)[-self.num:])
        logger.debug('writing left words')
        logger.debug(self.new_words[-self.num:])
        logger.debug('get new words')
        self.new_words = set(self.new_words[:-self.num])-self.known_words
        logger.debug(self.new_words)
        self.finish()

    def finish(self):
        CONFIG = self.config
        NEW_WORDS_EACH_ARTICLE_PATH = CONFIG['MAIN_PATH'] + \
            CONFIG['NEW_WORDS_EACH_ARTICLE_PATH']
        safe_IO.mv_file(self.file_path, CONFIG['MAIN_PATH'] +
                        CONFIG['OLD_ARTICLES_PATH'])
        safe_IO.write_each_words(
            NEW_WORDS_EACH_ARTICLE_PATH, self.name, self.new_words)
        with open(CONFIG['MAIN_PATH'] + CONFIG['OLD_WORDS_PATH'], 'w') as old:
            old.write('\n'.join(self.known_words))
        logger.debug('write new words to '+CONFIG['MAIN_PATH'] + CONFIG['NEW_WORDS_PATH'])
        with open(CONFIG['MAIN_PATH'] + CONFIG['NEW_WORDS_PATH'], 'a') as new:
            new.write('\n'.join(self.new_words))
