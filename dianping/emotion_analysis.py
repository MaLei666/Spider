#!/home/zkfr/.local/share/virtualenvs/xf-5EfV3Nly/bin/python
#-*- coding:utf-8 -*-
# @author : MaLei 
# @datetime : 2019-01-08 11:16
# @file : emotion_analysis.py
# @software : PyCharm

import pandas as pd
from matplotlib import pyplot as plt
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import roc_auc_score, f1_score
from sklearn.metrics import confusion_matrix
from imblearn.over_sampling import SMOTE


# data = pd.read_csv('data.csv')
# data.head()
#构建label值
def zhuanhuan(score):
    if score > 3:
        return 1
    elif score < 3:
        return 0
    else:
        return None

# data['target'] = data['stars'].map(lambda x:zhuanhuan(x))
# data_model = data.dropna()



















