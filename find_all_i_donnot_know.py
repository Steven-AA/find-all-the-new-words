#!python2
#coding:utf-8
import os
import re
# import msvcrt
# number_of_all_words = 0
def real_word(word):
    p = re.compile('[a-z,A-Z,\',‘]')
    a = p.findall(word)
    str = ''
    real_word = str.join(a)
    return real_word.lower()

def split_the_article(article):
    sep = re.compile('[\r\n., ]')
    words = re.split(sep,article)
    filcts = (real_word(word) for word in words)
    set_of_words = set(filcts)
    return set_of_words

def read_new_words(path,known_words):
    with open(path)as f:
        article = f.read()
    words = split_the_article(article)
    print('there are {} words in {}'.format(len(words),path))
    new_words = words - known_words
    num = len(new_words)
    if num == 0:
        print('No new word')
    elif num ==1:
        print('only1 new word')
    else:
        print(str(num)+' of them are new words')
    return new_words

def get_name(path):
    try:
        names = os.listdir(path)
    except:
        os.mkdir('../articles/')
        names = os.listdir(path)
    return names

def read_known_words():
    try:
        with open ('./old.txt')as f:
            all_the_words = f.read()
    except:
        print('\'old.txt\' missing......')
        all_the_words = ""
    known_words = split_the_article(all_the_words)
    print(known_words)
    num = len(known_words)
    print('There are ' + str(num)+' words I have known')
    return known_words

def my_input(output):
    try:
        judge = input(output)
    except:
        print('Input error! Plz try again:')
        judge = my_input(output)
    return judge

def learn(new_words,known_words):
    num = len(new_words)
    print('if you know the word print 1, else print 2')
    for word in new_words:
        num -=1
        judge = my_input(word+'('+str(num)+' Left)\n')
        if judge == 1:
            known_words.add(word)
    return new_words - known_words

def write_each_new_words(name,new_words):
    try:
        os.makedirs('./new_words_of_each_article/')
    except:
        pass
    try:
        with open('./new_words_of_each_article/'+name,'w') as f:
            f.write('\n'.join(new_words))
    except:
        print('failed to creat file of \'./new_words_of_each_article/'+name+'\'')

if __name__ =='__main__':
    flag = 3
    while flag != 1 and flag !=2:
        flag = input('print 1 to build model\nprint 2 to find model\nhere to get some help:https://zhuanlan.zhihu.com/p/25003457\n')
    new_word_all = set()
    known_words = read_known_words()
    path = r'./articles'
    file_names = get_name(path)
    print(file_names)
    for file_name in file_names:
        print('opening' + file_name + '......')
        path_1 = path + '/' + file_name
        new_words = read_new_words(path_1,known_words)
        if new_words:
            if flag == 1:
                new_words = learn(new_words,known_words)
                if new_words:
                    print('new words:')
                    print(new_words)
                    write_each_new_words(file_name,new_words)
                    new_word_all = new_word_all | set(new_words)
            else:
                new_word_all = new_word_all | set(new_words)
    with open('./old.txt','w') as old:
        old.write(' '.join(known_words))
    with open('./new.txt','w') as new:
        new.write('\n'.join(new_word_all))
    # print(ord(msvcrt.getch()))
