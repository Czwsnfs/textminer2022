from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import os,time
import base64
from io import BytesIO
import matplotlib
from sklearn.utils import resample
matplotlib.use('Agg')
import jieba 
import random
from gensim.models.word2vec import Word2Vec
from adjustText import adjust_text
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from matplotlib.font_manager import *
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def show(request):
    return render(request, "web03/index.html")



# 分词
def load_stop_words(file=r"./static/stopwords.txt"):
    with open(file,"r",encoding = "utf-8") as f:
        return f.read().split("\n")
# 训练语料库
@csrf_exempt
def train(request):
    myFile = request.FILES.get("myFile",None)
    if not myFile:
                return HttpResponse('没有要上传的文件') 
#生成上传后的文件名
    filename = str(time.time())+"."+myFile.name.split('.').pop()
    # filename = myFile.name
    des = open("./static/test/"+filename,"wb+")
    for chunk in myFile.chunks(): #分块读取上传文件内容并写入目标文件
        des.write(chunk)
    des.seek(0)
    stop_words = load_stop_words()
    result = []
    all_data = open("./static/test/"+filename,encoding='UTF-8')
    for words in all_data:
        c_words = jieba.lcut(words)
        result.append([word for word in c_words if word not in stop_words])
    num_features = 300    # Word vector dimensionality
    min_word_count=1   # Minimum word count
    num_workers =4       # Number of threads to run in parallel
    context=10         # Context window size
    model_name = "{}.model".format(time.strftime("%Y-%m-%d",time.localtime())+myFile.name)
    model = Word2Vec(result, workers=num_workers, \
            vector_size=num_features, min_count = min_word_count, \
            window = context,sg=1)
    model.save(os.path.join(r'./static/', 'model',
                               model_name))
    return HttpResponse("导入成功啦！")
# 可视化词向量
@csrf_exempt
def visual(request):
    a_title=request.POST.get("a_title")
    model_name = "{}.model".format(time.strftime("%Y-%m-%d",time.localtime())+a_title)
    model1='./static/model/'+model_name
    model=Word2Vec.load(model1)
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
    plt.figure(dpi=180)
    plt.scatter(embedd[:,0], embedd[:,1],s=7,c='royalblue')
    myfont=FontProperties(fname='C:\Windows\Fonts\simsun.ttc')
    for i in range(len(w)):
        x = embedd[i][0]
        y = embedd[i][1]
        text.append(plt.text(x, y, words[i]))
    adjust_text(text, 
                only_move={'text': 'x'},
                arrowprops=dict(arrowstyle='-', color='grey')
                )
    picname=a_title+'词向量可视化'
    plt.savefig('./static/png/'+picname+'.png')
    visualuzation= BytesIO()
    plt.savefig(visualuzation,format="png",dpi=300)
    plot_data = visualuzation.getvalue()
    imb = base64.b64encode(plot_data) # 对plot_data进行编码 
    ims = imb.decode('utf-8')
    plt.close()
    return JsonResponse('<img src="data:image/png; base64,%s"/>'%ims,safe=False)