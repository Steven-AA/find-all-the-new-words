import pytest
import pandas as pd
from safe_IO import *

def test_if_expect_key():
    assert if_expect_key('a', ['b'])==False
    assert if_expect_key('a', ['a','b'])==True

def test_load_lemmatization_list_to_dic():
    dic_data = pd.read_csv('./lemmatization-en.txt',sep='\t',header=None)
    value = list(dic_data.iloc[:,0])
    key = list(dic_data.iloc[:,1])
    fix_dic = dict(zip(key,value))
    assert load_lemmatization_list_to_dic('list')==fix_dic
    assert load_lemmatization_list_to_dic('NLTK')==None
