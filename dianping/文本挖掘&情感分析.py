#!/usr/bin/env python
# coding: utf-8

# # 大众点评评价情感分析~
# 先上结果：
# 
# | 糖水店的评论文本                             | 模型预测的情感评分 |
# | :------------------------------------------- | :----------------- |
# | '糖水味道不错，滑而不腻，赞一个，下次还会来' | 0.91               |
# | '味道一般，没啥特点'                         | 0.52               |
# | '排队老半天，环境很差，味道一般般'           | 0.05               |
# 
# 模型的效果还可以的样子，yeah~接下来我们好好讲讲怎么做的哈，我们通过爬虫爬取了大众点评广州8家最热门糖水店的3W条评论信息以及评分作为训练数据，前面的分析我们得知*样本很不均衡*。接下来我们的整体思路就是：文本特征处理(分词、去停用词、TF-IDF)—机器学习建模—模型评价。
# 
# 我们先不处理样本不均衡问题，直接建模后查看结果，接下来我们再按照两种方法处理样本不均衡，对比结果。
# 
# ### 数据读入和探索

# In[26]:


import pandas as pd
from matplotlib import pyplot as plt
import jieba
data = pd.read_csv('data.csv')
data.head()


# ### 构建标签值
# 
# 大众点评的评分分为1-5分，1-2为差评，4-5为好评，3为中评，因此我们把1-2记为0,4-5记为1,3为中评，对我们的情感分析作用不大，丢弃掉这部分
# 数据，但是可以作为训练语料模型的语料。我们的情感评分可以转化为标签值为1的概率值，这样我们就把情感分析问题转为文本分类问题了。
#构建label值
def zhuanhuan(score):
    if score > 3:
        return 1
    elif score < 3:
        return 0
    else:
        return None
    
#特征值转换
data['target'] = data['stars'].map(lambda x:zhuanhuan(x))
data_model = data.dropna()

# ### 文本特征处理
# 中文文本特征处理，需要进行中文分词，jieba分词库简单好用。
# 接下来需要过滤停用词，网上能够搜到现成的。
# 最后就要进行文本转向量，有词库表示法、TF-IDF、word2vec等，
# 这篇文章作了详细介绍，推荐一波 https://zhuanlan.zhihu.com/p/44917421
# 这里我们使用sklearn库的TF-IDF工具进行文本特征提取。
#切分测试集、训练集
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(data_model['cus_comment'], data_model['target'], random_state=3, test_size=0.25)

#引入停用词
infile = open("stopwords.txt",encoding='utf-8')
stopwords_lst = infile.readlines()
stopwords = [x.strip() for x in stopwords_lst]

#中文分词
def fenci(train_data):
    words_df = train_data.apply(lambda x:' '.join(jieba.cut(x)))
    return words_df

#使用TF-IDF进行文本转向量处理
from sklearn.feature_extraction.text import TfidfVectorizer
tv = TfidfVectorizer(stop_words=stopwords, max_features=3000, ngram_range=(1,2))
tv.fit(x_train)

# ### 机器学习建模
# 特征和标签已经准备好了，接下来就是建模了。这里我们使用文本分类的经典算法朴素贝叶斯算法，
# 而且朴素贝叶斯算法的计算量较少。特征值是评论文本经过TF-IDF处理的向量，标签值评论的分类共两类，
# 好评是1，差评是0。情感评分为分类器预测分类1的概率值。
#计算分类效果的准确率
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import roc_auc_score, f1_score
classifier = MultinomialNB()
classifier.fit(tv.transform(x_train), y_train)
classifier.score(tv.transform(x_test), y_test)

#计算分类器的AUC值
y_pred = classifier.predict_proba(tv.transform(x_test))[:,1]
roc_auc_score(y_test,y_pred)


#计算一条评论文本的情感评分
def ceshi(model,strings):
    strings_fenci = fenci(pd.Series([strings]))
    return float(model.predict_proba(tv.transform(strings_fenci))[:,1])

#从大众点评网找两条评论来测试一下
# test1 = '很好吃，环境好，所有员工的态度都很好，上菜快，服务也很好，味道好吃，都是用蒸馏水煮的，推荐，超好吃' #5星好评
# test2 = '糯米外皮不绵滑，豆沙馅粗躁，没有香甜味。12元一碗不值。' #1星差评
# print('好评实例的模型预测情感得分为{}\n差评实例的模型预测情感得分为{}'.format(ceshi(classifier,test1),ceshi(classifier,test2)))

# 可以看出，准确率和AUC值都非常不错的样子，但点评网上的实际测试中，
# 5星好评模型预测出来了，1星差评缺预测错误。为什么呢？我们查看一下**混淆矩阵**
from sklearn.metrics import confusion_matrix
y_predict = classifier.predict(tv.transform(x_test))
cm = confusion_matrix(y_test, y_predict)

# 可以看出，**负类的预测非常不准**，433单准确预测为负类的只有15.7%，应该是由于**数据不平衡**导致的，模型的默认阈值为输出值的中位数。比如逻辑回归的输出范围为[0,1]，当某个样本的输出大于0.5就会被划分为正例，反之为反例。在数据的类别不平衡时，采用默认的分类阈值可能会导致输出全部为正例，产生虚假的高准确度，导致分类失败。
# 处理样本不均衡问题的方法，首先可以选择调整阈值，使得模型对于较少的类别更为敏感，或者选择合适的评估标准，比如ROC或者F1，而不是准确度（accuracy）。另外一种方法就是通过采样（sampling）来调整数据的不平衡。其中欠采样抛弃了大部分正例数据，从而弱化了其影响，可能会造成偏差很大的模型，同时，数据总是宝贵的，抛弃数据是很奢侈的。另外一种是过采样，下面我们就使用过采样方法来调整。
# ### 过采样（单纯复制）
# 单纯的重复了反例，因此会过分强调已有的反例。如果其中部分点标记错误或者是噪音，那么错误也容易被成倍的放大。因此最大的风险就是对反例过拟合。

data['target'].value_counts()

#把0类样本复制10次，构造训练集
index_tmp = y_train==0
y_tmp = y_train[index_tmp]
x_tmp = x_train[index_tmp]
x_train2 = pd.concat([x_train,x_tmp,x_tmp,x_tmp,x_tmp,x_tmp,x_tmp,x_tmp,x_tmp,x_tmp,x_tmp])
y_train2 = pd.concat([y_train,y_tmp,y_tmp,y_tmp,y_tmp,y_tmp,y_tmp,y_tmp,y_tmp,y_tmp,y_tmp])

#使用过采样样本(简单复制)进行模型训练，并查看准确率
clf2 = MultinomialNB()
clf2.fit(tv.transform(x_train2), y_train2)
y_pred2 = clf2.predict_proba(tv.transform(x_test))[:,1]
roc_auc_score(y_test,y_pred2)

#查看此时的混淆矩阵
# y_predict2 = clf2.predict(tv.transform(x_test))
# cm = confusion_matrix(y_test, y_predict2)

# 可以看出，即使是简单粗暴的复制样本来处理样本不平衡问题，负样本的识别率大幅上升了，变为77%，满满的幸福感呀~我们自己写两句评语来看看

# ceshi(clf2,'排队人太多，环境不好，口味一般')

# 可以看出把0类别的识别出来了，太棒了~
# ### 过采样（SMOTE算法）
# SMOTE（Synthetic minoritye over-sampling technique,SMOTE），是在局部区域通过K-近邻生成了新的反例。相较于简单的过采样，SMOTE降低了过拟合风险，但同时运算开销加大
# 对SMOTE感兴趣的同学可以看下这篇文章https://www.jianshu.com/p/ecbc924860af

#使用SMOTE进行样本过采样处理
from imblearn.over_sampling import SMOTE
# oversampler=SMOTE(random_state=0)
# x_train_vec = tv.transform(x_train)
# x_resampled, y_resampled = oversampler.fit_sample(x_train_vec, y_train)
#
# #原始的样本分布
# y_train.value_counts()
#
# #经过SMOTE算法过采样后的样本分布情况
# pd.Series(y_resampled).value_counts()


# 我们经过插值，把0类数据也丰富为14923个数据了，这时候正负样本的比例为1:1，接下来我们用平衡后的数据进行训练，效果如何呢，好期待啊~

#使用过采样样本(SMOTE)进行模型训练，并查看准确率
# clf3 = MultinomialNB()
# clf3.fit(x_resampled, y_resampled)
# y_pred3 = clf3.predict_proba(tv.transform(x_test))[:,1]
# roc_auc_score(y_test,y_pred3)

#查看此时的准确率
# y_predict3 = clf3.predict(tv.transform(x_test))
# cm = confusion_matrix(y_test, y_predict3)
#
# #到网上找一条差评来测试一下情感评分的预测效果
# test3 = '糯米外皮不绵滑，豆沙馅粗躁，没有香甜味。12元一碗不值。'
# ceshi(clf3,test3)
# 可以看出，使用SMOTE插值与简单的数据复制比起来，AUC率略有提高，实际预测效果也挺好
# ### 模型评估测试
# 接下来我们把3W条数据都拿来训练，数据量变多了，模型效果应该会更好

#词向量训练
tv2 = TfidfVectorizer(stop_words=stopwords, max_features=3000, ngram_range=(1,2))
tv2.fit(data_model['cus_comment'])

#SMOTE插值
X_tmp = tv2.transform(data_model['cus_comment'])
y_tmp = data_model['target']
sm = SMOTE(random_state=0)
X,y = sm.fit_sample(X_tmp, y_tmp)

clf = MultinomialNB()
clf.fit(X, y)

def fenxi(strings):
    strings_fenci = fenci(pd.Series([strings]))
    return float(clf.predict_proba(tv2.transform(strings_fenci))[:,1])

a=fenxi('你奶奶个腿儿')
print(a)

# 只用到了简单的机器学习，就做出了不错的情感分析效果，知识的力量真是强大呀，666~
# ### 后续优化方向
# 
# - 使用更复杂的机器学习模型如神经网络、支持向量机等
# - 模型的调参
# - 行业词库的构建
# - 增加数据量
# - 优化情感分析的算法
# - 增加标签提取等
# - 项目部署到服务器上，更好地分享和测试模型的效果
