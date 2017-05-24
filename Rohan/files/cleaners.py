import json, string, enchant, nltk, datetime
import pandas as pd
import numpy as np
from collections import Counter
from bs4 import BeautifulSoup
from nltk.metrics import edit_distance

class SpellingReplacer(object):
    def __init__(self, dict_name = 'en_GB', max_dist = 2):
        self.spell_dict = enchant.Dict(dict_name)
        self.max_dist = 2

    def replace(self, word):
        if self.spell_dict.check(word):
            return word
        suggestions = self.spell_dict.suggest(word)

        if suggestions and edit_distance(word, suggestions[0]) <= self.max_dist:
            return suggestions[0]
        else:
            return word
def spell_check(word_list):
    checked_list = []
    for item in word_list:
        replacer = SpellingReplacer()
        r = replacer.replace(item)
        checked_list.append(r)
    return checked_list
def word_clean(words):
    text = BeautifulSoup(words, 'lxml')
    text = text.get_text()
    text = text.encode('ascii', 'replace').decode()
    text = str(' '.join(text.split('\n'))).lower()
    text = text.translate(None, string.punctuation)
    text = text.translate(None, string.digits)
    words = [word for word in text.split(' ') if word != '']
    spwords = spell_check(words)
    res = " ".join([word1 for word1, word2 in zip(words,spwords) if word1 == word2])
    return res

datecols = ['approx_payout_date','event_created', 'event_end', 'event_start', 'user_created']
convert = lambda x: datetime.datetime.fromtimestamp(x)
for i in datecols:
    df[i]=df[i].apply(pd.to_numeric)
    df[i]=df[i].apply(convert)
df['user_age'] = (df['user_age']/12).astype(int)
df['description2'] = df['description'].apply(word_clean)
