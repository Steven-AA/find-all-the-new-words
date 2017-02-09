#!python2
#coding:utf-8
import os
import re
import msvcrt
# number_of_all_words = 0
set_of_new_words = set()
known_words = set()
def real_word(word):
    p = re.compile('[a-z,A-Z,\',‘]')
    a = p.findall(word)
    str = ''
    real_word = str.join(a)
    return real_word.lower()

def split_the_article(article):
    sep = re.compile('[\r\n., ]')
    words = re.split(article)
    filcts = (real_word(word) for word in words)
    set_of_words = set(filcts)
    number_of_all_words = len(set_of_words)
    return set_of_words,number_of_all_words

def read_new_words(path,name):
    global known_words
    with open(path)as f:
        article = f.read()
    words,_ = split_the_article(article)
    print('there are {} words in {}'.format(num,name))
    new_words = words - known_words
    num = len(new_words)
    set_of_new_words = new_words + set_of_new_words
    if num == 0:
        print('No new word')
    elif num ==1:
        print('only1 new word')
    else:
        print(str(num)+' of them are new words')
    return num

def get_name(path):
    try:
        names = os.listdir(path)
    except:
        os.mkdir('../articles/')
        names = os.listdir(path)
    return names

def read_known_words():
    global known_words
    try:
        with open ('../old.txt')as f:
            all_the_words = f.read()
    except:
        print('\'old.txt\' missing......')
        all_the_words = ""
    known_words,num = split_the_article(all_the_words)
    print('There are ' + str(num)+' words I have known')
    return known_words

def my_input(output):
    try:
        judge = input(output)
    except:
        print('Input error! Plz try again:')
        judge = my_input(output)
    return judge

def learn(num):
    real_new_words = []
    global known_words,set_of_new_words
    print('if you know the word print 1, else print 2')
    for each_filct in set_of_new_words:
        num -=1
        judge = my_input(each_filct+'('+str(num)+' Left)\n')
        if judge == 1:
            known_words.add(each_filct)
            set_of_new_words.remove(each_filct)
    return set_of_new_words

def write_each_new_words(name):
    try:
        os.makedirs('../new_words_of_each_article/')
    except:
        pass
    try:
        f = open('../new_words_of_each_article/'+name,'w')
        return f
    except:
        print('failed to creat file of \'./new_words_of_each_article/'+name+'\'')

if __name__ =='__main__':
    flag = 3
    while flag != 1 and flag !=2:
        flag = input('print 1 to build model\nprint 2 to find model\nhere to get some help:https://zhuanlan.zhihu.com/p/25003457\n')
    new_word_all = []
    read_known_words()
    path = r'../articles'
    file_names = get_name(path)
    print(file_names)
    for each_filct in file_names:
        print('opening' + each_filct + '......')
        path_1 = path + '/' + each_filct
        num = read_new_words(path_1,each_filct)
        if not num == 0:
            if flag == 1:
                real_new_words = learn(num)
                if real_new_words:
                    print('new words:')
                    print(real_new_words)
                    f = write_each_new_words(each_filct)
                    for each_filct in real_new_words:
                        new_word_all.append(each_filct)
                        f.write(each_filct)
            else:
                for each_filct in set_of_new_words:
                        new_word_all.append(each_filct)
            set_of_new_words = set()
    with open('../old.txt','w') as old:
        old.write(' '.join(known_words))
    with open('../new.txt','w') as new:
        new.write('\n'.join(new_word_all))
    print(ord(msvcrt.getch()))
