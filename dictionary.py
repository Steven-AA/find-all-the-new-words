import requests
from bs4 import BeautifulSoup
import urllib
import logging
from googletrans import Translator,LANGUAGES

logger = logging.getLogger('FAIDK.Article')

def fix_result(a):
    to_fix = ["时 态","比较级","副 词","形容词","名 词"]
    for _ in to_fix:
        try:
            a = a[:a.index(_)-1]
        except:
            pass
    return a

def eudic(word):
    url = "https://dict.eudic.net/dicts/en/"+word
    headers = {"authority":"dict.eudic.net",
    "content-type":"application/x-www-form-urlencoded",
    "origin": "https://dict.eudic.net",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
            }
    r = requests.get(url,headers)
    soup = BeautifulSoup(r.text,"lxml")
    try:
        a = soup.find_all(id="ExpFCChild")[0].get_text("\t\n")
    except Exception as e:
        logger.warning(word+"  "+str(e))
        from nltk.stem import WordNetLemmatizer
        wordnet_lemmatizer = WordNetLemmatizer()
        word = wordnet_lemmatizer.lemmatize(word)
        url = "https://dict.eudic.net/dicts/en/"+word
        r = requests.get(url,headers)
        soup = BeautifulSoup(r.text,"lxml")
        try:
            a = soup.find_all(id="ExpFCChild")[0].get_text("\t\n")
            a = word+"\n\n"+a
        except Exception as e:
            logger.warning("fix failed  "+word+"  "+str(e))
            return ""
    if a[0] == u"赞":
        a = a[a.index(")")+3:]
    a = fix_result(a)
    a = a.replace(".\t\n",".\t")
    return a

def google(text):
    translator = Translator()
    return translator.translate(text,LANGUAGES["zh-cn"]).text