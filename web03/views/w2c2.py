from django.views.decorators.csrf import csrf_exempt
from sklearn.manifold import TSNE
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import *
import random
from gensim.models.word2vec import Word2Vec
from django.shortcuts import render
from django.http import HttpResponse,FileResponse
import matplotlib
matplotlib.use('Agg')
import numpy as np
import os,time,csv
from adjustText import adjust_text
from django.views.decorators.csrf import csrf_exempt
# 导出图片
@csrf_exempt
def pic_download(request):
    a_title=request.POST.get("a_title")
    model_name = "{}.model".format(time.strftime("%Y-%m-%d",time.localtime())+a_title)
    # name(request)
    model1='./static/model/'+model_name
    model=Word2Vec.load(model1)
    picname=a_title+'词向量可视化'
    # file =Path("./static/test/"+picname+'.png')
    if os.access("./static/png/"+picname+'.png',os.X_OK):
        file1=open("./static/png/"+picname+'.png','rb')
        # img=base64.b64encode(file1.read())
        response=FileResponse(file1)
        response['Content-Type']='image/png'
        response['Content-Disposition']='attachment;filename="visualuzation.png"'
        return response
    if not os.access("./static/test/"+picname+'.png',os.X_OK):
        words = list(model.wv.index_to_key)
        if (len(words)<=100):
            w=random.sample(words,len(words))
        elif(100<=len(words)<=200):
            w=random.sample(words,100)
        else:
            w=random.sample(words,130)
        vector = model.wv[w]
        tsne = TSNE(n_components = 2, random_state=23, perplexity =40, learning_rate =1000, n_iter = 500)
        embedd = tsne.fit_transform(vector)
        text=[]
        plt.style.use('seaborn')
        plt.rcParams['font.sans-serif']=['SimHei']
        plt.rcParams['axes.unicode_minus']=False
        plt.figure(dpi=140)
        plt.scatter(embedd[:,0], embedd[:,1],s=7,c='royalblue')
        for i in range(len(w)):
            x = embedd[i][0]
            y = embedd[i][1]
            text.append(plt.text(x, y, words[i]))
        adjust_text(text, 
                    only_move={'text': 'x'},
                    arrowprops=dict(arrowstyle='-', color='grey')
                    )
        plt.savefig('./static/png/'+picname+'.png')
        file1=open("./static/png/"+picname+'.png','rb')
        response=FileResponse(file1)
        response['Content-Type']='image/png'
        response['Content-Disposition']='attachment;filename="visualuzation.png"'
        return response
# 导出词表
@csrf_exempt
def cibiao_download(request): 
     #下载词表
    a_title=request.POST.get("a_title")
    model_name = "{}.model".format(time.strftime("%Y-%m-%d",time.localtime())+a_title)
    model1='./static/model/'+model_name
    model=Word2Vec.load(model1)
    # model = Word2Vec.load(r'G:\\TextMiner-master\model\model\300features_40minwords_10context.model')
    try:
        word_list=[]
        word_list.append(model.wv.index_to_key)
        word_list=np.array(word_list).reshape(len(model.wv.index_to_key))
        response = HttpResponse(content_type='text/csv')#告诉浏览器是text/csv格式
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'# csv文件名，不影响
        writer = csv.writer(response)
        writer.writerow(['词表'])
        for data in word_list:
            writer.writerow([data])
        return response
    except:
        return HttpResponse("载入错误！")


