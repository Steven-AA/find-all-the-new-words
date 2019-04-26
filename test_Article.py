import pytest
import Article
import safe_IO
import os

def test_if_sorted():
    with open('./articles/test.txt','w') as t:
        t.write('c b a')
    with open('./old.txt','w') as t:
        t.write('b')
    CONFIG = safe_IO.load_json('./FAIDK.config')
    article = Article.Article(CONFIG, 'test.txt', '2')
    assert article.new_words== ['a','c']

def test_if_learn_quit():
    clear_all()
    with open('./articles/test.txt','w') as t:
        t.write('a b c d')
    CONFIG = safe_IO.load_json('./FAIDK.config')
    article = Article.Article(CONFIG, 'test.txt', '1')
    with open('old.txt') as o:
        assert o.read() == '\na'
    with open('new.txt') as n:
        assert n.read() == 'b'
    with open('./articles/l_test.txt') as n:
        assert n.read() == 'c\nd'
    clear_all()

def clear_all():
    os.system("rm ./old_articles/*")
    os.system("rm ./new_words_of_each_article/*")
    os.system("rm ./articles/*")
    os.system("rm ./new.txt")
    os.system("rm ./old.txt")