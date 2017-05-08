# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 13:25:07 2017

@author: YoungHao
"""

import math
import pickle

corpus_list = []
corpus = ''
reverse_corpus = ''
wordDic = {}
reverse_wordDic = {}               #反序语料，计算左邻字信息熵
right_word_entropy = {}
left_word_entropy = {}
probability_word = {}
concreation_word = {}
score = {}
#stop_symbol = '()，．。！,ゅ\'～~`·？-=:、；[]{}*&^%$#@!~+_=-！@#￥%……&*（）——+}{【】||？。><！，;.1234567890：“”"》《+?/%）（@ \n \t \u3000'

for lines in open("红楼梦.txt", encoding = 'utf-8'):
    corpus_list.append(lines)
    i = i + 1
    if(i % 2000 == 0):
        print(i)
    
corpus = ''.join(corpus_list)    #使用list保存string，然后用join方法来合并，效率比"+"更高
reverse_corpus = corpus[::-1]
print(len(corpus))
print(len(reverse_corpus))
def dictionary(w):                 #w：词语最大长度，建立备选词典
    end = int(len(corpus))     #语料长度
    for f in range(w):
        j = f + 1
        i = 0
        flag = 0
        while( j < end ):
            word = str(corpus[i:j])
 #           for s in stop_symbol:
 #               if s in word:
 #                   flag = 1
            if flag == 0:
                if word.strip() not in wordDic:
                    try:
                        wordDic[word] = 1
                    except Exception:
                        continue
                else:
                    try:
                        wordDic[word] += 1
                    except Exception:
                        continue
            i += 1
            j += 1
            flag = 0
    end = int(len(reverse_corpus))     #逆序语料长度
    for f in range(w):
        j = f + 1
        i = 0
        flag = 0
        while( j < end ):
            word = str(reverse_corpus[i:j])
#            for s in stop_symbol:
#                if s in word:
#                    flag = 1
            if flag == 0:
                if word.strip() not in reverse_wordDic:
                    try:
                        reverse_wordDic[word] = 1
                    except Exception:
                        continue                    
                else:
                    try:
                        reverse_wordDic[word] += 1
                    except Exception:
                        continue 
            i += 1
            j += 1
            flag = 0
def entropy(): 
    #先计算右邻字信息熵
    sorted_WordDic = sorted(wordDic)       #右邻字信息熵
    i = 0
    length_wordDic = len(sorted_WordDic)
    while (i < length_wordDic):
        word = sorted_WordDic[i]             #目标词语
        j = i + 1
        if ( j >= length_wordDic):
            break
        buffer = {}                         #右邻字及个数 
        while (word in sorted_WordDic[j]):
            label = sorted_WordDic[j][len(word)]
            if label not in buffer:
                buffer[label] = wordDic[sorted_WordDic[j]]     #不要重复加相关右邻字                 
            j += 1
            if ( j >= length_wordDic):
                break
        sum = 0.000000001
        pro_buffer = {}
        for buff in buffer:
            sum = sum + buffer[buff]
        for buff in buffer:
            pro_buffer[buff] = buffer[buff] / sum
        right_entropy = 0.0
        for pro in pro_buffer:
            right_entropy = right_entropy - pro_buffer[pro] * math.log(pro_buffer[pro])
        right_word_entropy[word] = right_entropy            #保存右邻字信息熵信息
        i += 1
        
    #再计算左邻字信息熵
    left_sorted_WordDic = sorted(reverse_wordDic)       #左邻字信息熵
    i = 0
    length_wordDic = len(left_sorted_WordDic) 
    while (i < length_wordDic):
        word = left_sorted_WordDic[i]             #目标词语
        j = i + 1
        if ( j >= length_wordDic):
            break
        buffer = {}                         #左邻字个数 
        while (word in left_sorted_WordDic[j]):
            label = left_sorted_WordDic[j][len(word)]
            if label not in buffer:
                buffer[label] = reverse_wordDic[left_sorted_WordDic[j]]     #不要重复加相关左邻字                 
            j += 1
            if ( j >= length_wordDic):
                break
        sum = 0.000000001
        pro_buffer = {}
        for buff in buffer:
            sum = sum + buffer[buff]
        for buff in buffer:
            pro_buffer[buff] = buffer[buff] / sum
        left_entropy = 0.0
        for pro in pro_buffer:
            left_entropy = left_entropy - pro_buffer[pro] * math.log(pro_buffer[pro])
        words = word[::-1]
        left_word_entropy[words] = left_entropy            #保存左邻字信息熵信息    
        i += 1
def concreation():                #计算完整词语凝固程度
    sum = 0.0
    for i in wordDic:
        sum = sum + wordDic[i]
    for i in wordDic:
        probability_word[i] = wordDic[i] / sum
    for i in wordDic:
        length = len(i)
        if length > 1:
            j = 1
            p = 9999999999
            while (j < length):
                right = i[0:j]
                left = i[j:length]
                k = probability_word[i] / (probability_word[right] * probability_word[left])
                if (p > k):
                    p = k
                j += 1
            concreation_word[i] = p
def word_generation(left_entropy, right_entropy, concreation):
    for word in wordDic:
        if ((len(word)) > 1 and (word in left_word_entropy) and (word in right_word_entropy) and (word in concreation_word)):
            if ((left_word_entropy[word] >= left_entropy) and (right_word_entropy[word] >= right_entropy) and (concreation_word[word] >= concreation)):
                print(word)
                score[word] = concreation_word[word] / left_word_entropy[word] / right_word_entropy[word]

dictionary(5)               #最大长度五个字的词语,参数可调
entropy()                   #计算左右信息熵
concreation()               #计算内部凝固程度
word_generation(0.2, 0.2, 300)       #参数可自行调整

def score2pickle():
    with open('score_word.pickle', 'wb') as f:
        pickle.dump(score, f)
        print('sucess')

score2pickle()


