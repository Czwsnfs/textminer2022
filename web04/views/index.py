#coding:utf-8
from django.http import HttpResponse
from django.shortcuts import redirect, render
import time,os
import numpy as np
from gensim import corpora, models
import jieba.posseg as jp, jieba
import pyLDAvis.gensim_models
from gensim.corpora.dictionary import Dictionary
from gensim import corpora, models
import pyLDAvis.gensim_models
from gensim.models.coherencemodel import CoherenceModel
from gensim.models.ldamodel import LdaModel
def LDA1(request):
    return render(request, "web04/LDA1.html")
def analyze12(request):
    doc1 = request.POST.get('txt',None)
    if not doc1:
        return HttpResponse("没有输入分析内容")
    doc_complete = [doc1]
    texts=doc_complete
    from gensim import corpora, models
    import numpy as np
    import pyLDAvis.gensim_models
    import jieba.posseg as jp,jieba
    from gensim.models.coherencemodel import CoherenceModel
    from gensim.models.ldamodel import LdaModel
    from gensim.corpora.dictionary import Dictionary
    import random
    flags = ('n', 'nr', 'ns', 'nt', 'eng', 'v', 'd','vn','vd')
    # 停用词表
    stopwords = open("C:\\Users\\86150\\Desktop\\Text Miner\\中文停用词.txt","r",encoding='utf-8').read()
    # 分词
    words_ls = []
    for text in texts:
        # 采用jieba进行分词
        words = [word.word for word in jp.cut(text) if word.flag in flags and word.word not in stopwords]
        words_ls.append(words)

    # 构造词典
    dictionary = Dictionary(words_ls)
    # 基于词典，使【词】→【稀疏向量】，并将向量放入列表，形成【稀疏向量集】
    corpus = [dictionary.doc2bow(words) for words in words_ls]
    corpus_tfidf = models.TfidfModel(corpus)[corpus]
    # lda模型，num_topics设置主题的个数
    a=5
    lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=a, random_state=100, iterations=50)
    # U_Mass Coherence
    ldaCM = CoherenceModel(model=lda, corpus=corpus, dictionary=dictionary, coherence='u_mass')
    doc_topic = [a for a in lda[corpus_tfidf]]#doc_topic 文档主题
    import os
    import csv
    #save csv
    fn = "C:\\Users\\86150\\Desktop\\LDAdemo\\static\\test\\alltopic.csv"
    num_topics=20
    m="w"
    i=0
    # save topic, term, prob data in the file
    with open(fn, "w", encoding="utf8", newline='') as csvfile:
        fieldnames = ["序号","topic", "prob"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if (m == "w"):
            writer.writeheader()
        print(doc_topic[0])
        for topicid,prob in doc_topic[0]:
            row = {}
            prob1=np.round(prob,5)
            i=i+1
            row['序号']=i
            #row['x']=random.uniform(-100,100)
            #row['y']=random.uniform(-100,100)
            row['topic'] = "topic"+str(topicid)
            row['prob'] = prob1
            writer.writerow(row)
    import csv
    import json
    # 指定encodeing='utf-8'中文防止乱码
    csvfile = open('C:\\Users\\86150\\Desktop\\LDAdemo\\static\\test\\alltopic.csv','r', encoding='utf-8')
    jsonfile = open('C:\\Users\\86150\\Desktop\\LDAdemo\\static\\test\\alltopic.json', 'w',encoding='utf-8')
    # 指定列名
    #fieldnames = ["x","y","topic", "prob"]
    reader = csv.DictReader( csvfile)
    # 指定ensure_ascii=False 为了不让中文显示为ascii字符码
    out = json.dumps( [ row for row in reader ] ,ensure_ascii=False)
    jsonfile.write(out)
    import os
    import csv
    #save csv
    fn = "C:\\Users\\86150\\Desktop\\LDAdemo\\static\\test\\topic_terms11.csv"
    num_topics=20
    m="w"
    i=0
    # save topic, term, prob data in the file
    with open(fn, "w", encoding="utf8", newline='') as csvfile:
        fieldnames = ["序号","topic_id", "term", "prob"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if (m == "w"):
            writer.writeheader()
        for topic_id in range(a):
            term_probs = lda.show_topic(topic_id, topn=12)
            print(term_probs)
            for term, pro in term_probs:
                row = {}
                prob1=np.round(pro,5)
                i=i+1
                row['序号']=i
                row['topic_id'] ="topic"+str(topic_id)
                row['prob'] = prob1
                row['term'] = term
                writer.writerow(row)
    import csv
    import json
    # 指定encodeing='utf-8'中文防止乱码
    csvfile = open('C:\\Users\\86150\\Desktop\\LDAdemo\\static\\test\\topic_terms11.csv','r', encoding='utf-8')
    jsonfile = open('C:\\Users\\86150\\Desktop\\LDAdemo\\static\\test\\topic_terms11.json', 'w',encoding='utf-8')
    # 指定列名
    #fieldnames = ["topic_id", "term", "prob"]
    reader = csv.DictReader( csvfile)
    # 指定ensure_ascii=False 为了不让中文显示为ascii字符码
    out = json.dumps( [ row for row in reader ] ,ensure_ascii=False)
    jsonfile.write(out)
    #filename1='C:\\Users\\86150\\Desktop\\LDAdemo\\static\\test\\topic_terms11.csv'
    #data=pd.read_csv(filename1)
    #xaxis=[i for i in range(0,20)]
    #topic_id=data[topic_id].value.tolist()
    #term=data[term].value.tolist()
    #prob=data[prob].value.tolist()
    return render(request, "web04/LDA2.html")
def analyze1(request):
    receive_file = request.FILES.get("pic",None)
    if not receive_file:
        return HttpResponse("没有上传文件信息")
#生成上传后的文件名
    filename ="LDA主题分析"
    des = open("./static/test/"+filename,"wb+")
    for chunk in receive_file.chunks(): #分块读取上传文件内容并写入目标文件
        des.write(chunk)
    des.seek(0)
    texts=des.readlines()
    from gensim import corpora, models
    import numpy as np
    import pyLDAvis.gensim_models
    import jieba.posseg as jp,jieba
    from gensim.models.coherencemodel import CoherenceModel
    from gensim.models.ldamodel import LdaModel
    from gensim.corpora.dictionary import Dictionary
    import random
    flags = ('n', 'nr', 'ns', 'nt', 'eng', 'v', 'd','vn','vd')
    # 停用词表
    stopwords = open("C:\\Users\\86150\\Desktop\\Text Miner\\中文停用词.txt","r",encoding='utf-8').read()
    # 分词
    words_ls = []
    for text in texts:
        # 采用jieba进行分词
        words = [word.word for word in jp.cut(text) if word.flag in flags and word.word not in stopwords]
        words_ls.append(words)

    # 构造词典
    dictionary = Dictionary(words_ls)
    # 基于词典，使【词】→【稀疏向量】，并将向量放入列表，形成【稀疏向量集】
    corpus = [dictionary.doc2bow(words) for words in words_ls]
    corpus_tfidf = models.TfidfModel(corpus)[corpus]
    # lda模型，num_topics设置主题的个数
    a=5
    lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=a, random_state=100, iterations=50)
    # U_Mass Coherence
    ldaCM = CoherenceModel(model=lda, corpus=corpus, dictionary=dictionary, coherence='u_mass')
    doc_topic = [a for a in lda[corpus_tfidf]]#doc_topic 文档主题
    import os
    import csv
    #save csv
    fn = "C:\\Users\\86150\\Desktop\\LDAdemo\\static\\test\\alltopic.csv"
    num_topics=20
    m="w"
    i=0
    # save topic, term, prob data in the file
    with open(fn, "w", encoding="utf8", newline='') as csvfile:
        fieldnames = ["序号","topic", "prob"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if (m == "w"):
            writer.writeheader()
        print(doc_topic[0])
        for topicid,prob in doc_topic[0]:
            row = {}
            prob1=np.round(prob,5)
            i=i+1
            row['序号']=i
            #row['x']=random.uniform(-100,100)
            #row['y']=random.uniform(-100,100)
            row['topic'] = "topic"+str(topicid)
            row['prob'] = prob1
            writer.writerow(row)
    import csv
    import json
    # 指定encodeing='utf-8'中文防止乱码
    csvfile = open('C:\\Users\\86150\\Desktop\\LDAdemo\\static\\test\\alltopic.csv','r', encoding='utf-8')
    jsonfile = open('C:\\Users\\86150\\Desktop\\LDAdemo\\static\\test\\alltopic.json', 'w',encoding='utf-8')
    # 指定列名
    #fieldnames = ["x","y","topic", "prob"]
    reader = csv.DictReader( csvfile)
    # 指定ensure_ascii=False 为了不让中文显示为ascii字符码
    out = json.dumps( [ row for row in reader ] ,ensure_ascii=False)
    jsonfile.write(out)
    import os
    import csv
    #save csv
    fn = "C:\\Users\\86150\\Desktop\\LDAdemo\\static\\test\\topic_terms11.csv"
    num_topics=20
    m="w"
    i=0
    # save topic, term, prob data in the file
    with open(fn, "w", encoding="utf8", newline='') as csvfile:
        fieldnames = ["序号","topic_id", "term", "prob"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if (m == "w"):
            writer.writeheader()
        for topic_id in range(a):
            term_probs = lda.show_topic(topic_id, topn=12)
            print(term_probs)
            for term, pro in term_probs:
                row = {}
                prob1=np.round(pro,5)
                i=i+1
                row['序号']=i
                row['topic_id'] ="topic"+str(topic_id)
                row['prob'] = prob1
                row['term'] = term
                writer.writerow(row)
    import csv
    import json
    # 指定encodeing='utf-8'中文防止乱码
    csvfile = open('C:\\Users\\86150\\Desktop\\LDAdemo\\static\\test\\topic_terms11.csv','r', encoding='utf-8')
    jsonfile = open('C:\\Users\\86150\\Desktop\\LDAdemo\\static\\test\\topic_terms11.json', 'w',encoding='utf-8')
    reader = csv.DictReader( csvfile)
    out = json.dumps( [ row for row in reader ] ,ensure_ascii=False)
    jsonfile.write(out)
    des.close()
    return render(request, "web04/LDA2.html")
def analyze11(request):
    a= request.POST.get('a')
    a=int(a)
    b= request.POST.get('b')
    b=int(b)
#生成上传后的文件名
    filename ="LDA主题分析"
    des = open("./static/test/"+filename,encoding='utf-8')
    des.seek(0)
    texts=des.readlines()
    from gensim import corpora,models
    import numpy as np
    import jieba.posseg as jp,jieba
    from gensim.models.coherencemodel import CoherenceModel
    from gensim.models.ldamodel import LdaModel
    from gensim.corpora.dictionary import Dictionary
    import random
    flags = ('n', 'nr', 'ns', 'nt', 'eng', 'v', 'd','vn','vd')
    # 停用词表
    stopwords = open("C:\\Users\\86150\\Desktop\\Text Miner\\中文停用词.txt","r",encoding='utf-8').read()
    # 分词
    words_ls = []
    for text in texts:
        # 采用jieba进行分词
        words = [word.word for word in jp.cut(text) if word.flag in flags and word.word not in stopwords]
        words_ls.append(words)

    # 构造词典
    dictionary = Dictionary(words_ls)
    # 基于词典，使【词】→【稀疏向量】，并将向量放入列表，形成【稀疏向量集】
    corpus = [dictionary.doc2bow(words) for words in words_ls]
    corpus_tfidf = models.TfidfModel(corpus)[corpus]
    # lda模型，num_topics设置主题的个数
    #a=5
    lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=a, random_state=100, iterations=50)
    # U_Mass Coherence
    ldaCM = CoherenceModel(model=lda, corpus=corpus, dictionary=dictionary, coherence='u_mass')
    doc_topic = [a for a in lda[corpus_tfidf]]#doc_topic 文档主题
    import os
    import csv
    #save csv
    fn = "C:\\Users\\86150\\Desktop\\LDAdemo\\static\\test\\alltopic.csv"
    num_topics=20
    m="w"
    i=0
    # save topic, term, prob data in the file
    with open(fn, "w", encoding="utf8", newline='') as csvfile:
        fieldnames = ["序号","topic", "prob"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if (m == "w"):
            writer.writeheader()
        print(doc_topic[0])
        for topicid,prob in doc_topic[0]:
            row = {}
            prob1=np.round(prob,5)
            #row['x']=random.uniform(-1,1)
            #row['y']=random.uniform(-1,1)
            row["序号"]=i+1
            row['topic'] = "topic"+str(topicid)
            row['prob'] = prob1
            writer.writerow(row)
    import csv
    import json
    # 指定encodeing='utf-8'中文防止乱码
    csvfile = open('C:\\Users\\86150\\Desktop\\LDAdemo\\static\\test\\alltopic.csv','r', encoding='utf-8')
    jsonfile = open('C:\\Users\\86150\\Desktop\\LDAdemo\\static\\test\\alltopic.json', 'w',encoding='utf-8')
    # 指定列名
    #fieldnames = ["x","y","topic", "prob"]
    reader = csv.DictReader( csvfile)
    # 指定ensure_ascii=False 为了不让中文显示为ascii字符码
    out = json.dumps( [ row for row in reader ] ,ensure_ascii=False)
    jsonfile.write(out)
    import os
    import csv
    #save csv
    fn = "C:\\Users\\86150\\Desktop\\LDAdemo\\static\\test\\topic_terms11.csv"
    num_topics=20
    m="w"
    i=0
    # save topic, term, prob data in the file
    with open(fn, "w", encoding="utf8", newline='') as csvfile:
        fieldnames = ["序号","topic_id", "term", "prob"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if (m == "w"):
            writer.writeheader()
        for topic_id in range(a):
            term_probs = lda.show_topic(topic_id, topn=b)
            print(term_probs)
            for term, pro in term_probs:
                row = {}
                prob1=np.round(pro,5)
                row["序号"]=i+1
                row['topic_id'] ="topic"+str(topic_id)
                row['prob'] = prob1
                row['term'] = term
                writer.writerow(row)
    import csv
    import json
    # 指定encodeing='utf-8'中文防止乱码
    csvfile = open('C:\\Users\\86150\\Desktop\\LDAdemo\\static\\test\\topic_terms11.csv','r', encoding='utf-8')
    jsonfile = open('C:\\Users\\86150\\Desktop\\LDAdemo\\static\\test\\topic_terms11.json', 'w',encoding='utf-8')
    # 指定列名
    #fieldnames = ["topic_id", "term", "prob"]
    reader = csv.DictReader( csvfile)
    # 指定ensure_ascii=False 为了不让中文显示为ascii字符码
    out = json.dumps( [ row for row in reader ] ,ensure_ascii=False)
    jsonfile.write(out)
    #filename1='C:\\Users\\86150\\Desktop\\LDAdemo\\static\\test\\topic_terms11.csv'
    #data=pd.read_csv(filename1)
    #xaxis=[i for i in range(0,20)]
    #topic_id=data[topic_id].value.tolist()
    #term=data[term].value.tolist()
    #prob=data[prob].value.tolist()
    return render(request, "web04/LDA2.html")
def analyze13(request):
    a= request.POST.get('a')
    a=str(a)
    b= request.POST.get('b')
    b=str(b)
#生成上传后的文件名
    import csv
    import json
    # 指定encodeing='utf-8'中文防止乱码
    import pandas as pd
    import pandas as pd
    file="C:\\Users\\86150\\Desktop\\LDAdemo\\static\\test\\alltopic.csv"
    df= pd.read_csv(file,index_col =u'序号')
    df.loc[df['topic']==a,'topic']=b
    df.to_csv(file)
    csvfile = open('C:\\Users\\86150\\Desktop\\LDAdemo\\static\\test\\alltopic.csv','r', encoding='utf-8')
    jsonfile = open('C:\\Users\\86150\\Desktop\\LDAdemo\\static\\test\\alltopic.json', 'w',encoding='utf-8')
    # 指定列名  
    #fieldnames = ["序号","x","y","topic", "prob"]
    reader = csv.DictReader(csvfile)
    # 指定ensure_ascii=False 为了不让中文显示为ascii字符码
    out = json.dumps( [ row for row in reader ] ,ensure_ascii=False)
    jsonfile.write(out)
    import os
    import csv
    #save csv
    # 指定encodeing='utf-8'中文防止乱码
    file1='C:\\Users\\86150\\Desktop\\LDAdemo\\static\\test\\topic_terms11.csv'
    df1= pd.read_csv(file1,index_col =u'序号')
    df1.loc[df1['topic_id']==a,'topic_id']=b
    df1.to_csv(file1)
    csvfile = open('C:\\Users\\86150\\Desktop\\LDAdemo\\static\\test\\topic_terms11.csv','r', encoding='utf-8')
    jsonfile = open('C:\\Users\\86150\\Desktop\\LDAdemo\\static\\test\\topic_terms11.json', 'w',encoding='utf-8')
    # 指定列名
    #fieldnames = ["序号","topic_id", "term", "prob"]
    reader = csv.DictReader( csvfile)
    # 指定ensure_ascii=False 为了不让中文显示为ascii字符码
    out = json.dumps( [ row for row in reader ] ,ensure_ascii=False)
    jsonfile.write(out)
    #filename1='C:\\Users\\86150\\Desktop\\LDAdemo\\static\\test\\topic_terms11.csv'
    #data=pd.read_csv(filename1)
    #xaxis=[i for i in range(0,20)]
    #topic_id=data[topic_id].value.tolist()
    #term=data[term].value.tolist()
    #prob=data[prob].value.tolist()
    return render(request, "web04/LDA2.html")
def analyze2(request):
    doc1 = request.POST.get('oneText',None)
    doc_complete = [doc1]
    twotext = {}
    file_object2=doc_complete
    data_set=[]  #建立存储分词的列表
    for i in range(len(file_object2)):
        result=[]
        seg_list = file_object2[i].split()
        for w in seg_list :  #读取每一行分词
            result.append(w)
        data_set.append(result)
    print(data_set)
    from gensim.models import doc2vec,ldamodel
    from gensim import corpora
    # 创建语料的词语词典，每个单独的词语都会被赋予一个索引
    dictionary = corpora.Dictionary(data_set)
    # 使用上面的词典，将转换文档列表（语料）变成 DT 矩阵
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in data_set]
    import gensim
    Lda = gensim.models.ldamodel.LdaModel
    # 在 DT 矩阵上运行和训练 LDA 模型
    ldamodel = Lda(doc_term_matrix, num_topics=3, id2word = dictionary, passes=50)
    #topic_list=lda.print_topics()
    txt=ldamodel.print_topics(num_topics=3, num_words=8)
    twotext['text1'] = doc_complete
    twotext['text2'] = txt
    return render(request, "web04/LDA2.html", twotext)
