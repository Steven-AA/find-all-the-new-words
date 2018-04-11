import re
class Article(object):
    def __init__(self, path):
        self.file_path = path
        self.article = self.read_article()
        self.words = self.split_the_article()
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

    def split_the_article(self):
        '''
        split the article
        '''
        sep = re.compile('[\r\n., ]')
        words = re.split(sep, self.article)
        filcts = (self.real_word(word) for word in words)
        set_of_words = set(filcts)
        print('there are {} words in {}'.format(len(set_of_words), self.file_path))
        return set_of_words

    def read_new_words(self, known_words):
        '''
        read new words from article
        '''
        new_words = self.words - known_words
        num = len(new_words)
        if num == 0:
            print('No new word')
        elif num == 1:
            print('only 1 new word')
        else:
            print(str(num) + ' new words')
        return new_words