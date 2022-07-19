from django.views.decorators.csrf import csrf_exempt
import numpy as np
from matplotlib.font_manager import *
from gensim.models.word2vec import Word2Vec
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import matplotlib
matplotlib.use('Agg')
import numpy as np
import time
import plotly as py
import plotly.graph_objs as go
from sklearn.decomposition import PCA
from django.views.decorators.csrf import csrf_exempt
def append_list(sim_words, words):
    list_of_words = []
    for i in range(len(sim_words)):
        sim_words_list = list(sim_words[i])
        sim_words_list.append(words)
        sim_words_tuple = tuple(sim_words_list)
        list_of_words.append(sim_words_tuple)
    return list_of_words
@csrf_exempt
def sim_visual(request):
#     input_word='汽车,市场'
    a_title=request.POST.get("a_title")
    model_name = "{}.model".format(time.strftime("%Y-%m-%d",time.localtime())+a_title)
    model1='./static/model/'+model_name
    model=Word2Vec.load(model1)
    word=request.POST.get('word')
    n=request.POST.get('n')
    n=int(n)
    topn=n
    user_input = [x.strip() for x in word.split('，')]
    result_word = []
    try:
        for u in user_input:

                sim_words = model.wv.most_similar(u, topn = n)
                sim_words = append_list(sim_words, u)

                result_word.extend(sim_words)

        similar_word = [word[0] for word in result_word]
        similarity = [word[1] for word in result_word] 
        similar_word.extend(user_input)
        words = [ word for word in similar_word ]
        word_vectors = np.array([model.wv[w] for w in words])

        three_dim = PCA(random_state=0).fit_transform(word_vectors)[:,:2]
        data = []
        count = 0
        for i in range (len(user_input)):
                    trace = go.Scatter(
                        x = three_dim[count:count+topn,0], 
                        y = three_dim[count:count+topn,1],  
    #                     z = three_dim[count:count+topn,2],
                        text = words[count:count+topn],
                        name = user_input[i],
                        textposition = "top center",
                        textfont_size = 13,
                        mode = 'markers+text',
                        marker = {
                            'size': 8,
                            'opacity': 0.8,
                            'color': 2
                        }

                    )

                    #对于2D，不是使用go.Scatter3d，我们需要用go.Scatter并删除变量z。另外，不要使用变量three_dim，而是使用前面声明的变量(例如two_dim)

                    data.append(trace)
                    count = count+topn

        trace_input = go.Scatter(
                        x = three_dim[count:,0], 
                        y = three_dim[count:,1],  
    #                     z = three_dim[count:,2],
                        text = words[count:],
                        name = '输入词',
                        textposition = "middle center",
                        textfont_size =16,
                        mode = 'markers+text',
                        marker = {
                            'size': 9,
                            'opacity': 0.8,
                            'color': '#75664d'
                        }
                        )

        # 对于2D，不是使用go.Scatter3d，我们需要用go.Scatter并删除变量z。另外，不要使用变量three_dim，而是使用前面声明的变量(例如two_dim)

        data.append(trace_input)

    # 配置布局

        layout = go.Layout(
            plot_bgcolor='rgb(245,245,245)',
            margin = {'l': 5, 'r': 0, 'b': 0, 't': 30},
            showlegend=True,
            legend=dict(
            x=1,
            y=0.5,
            font=dict(
                family="Courier New",
                size=10,
                color="black"
            )),
            font = dict(
                family = " Courier New ",
                size = 10),
            autosize = False,
            width = 550,
            height = 330
        )  
        plot_figure = go.Figure(data = data, layout = layout)
        pyplt=py.offline.plot
        div=pyplt(plot_figure,output_type='div',auto_open=False,show_link=False)
        context={}
        context['graph']=div
        return JsonResponse(context)
    except:
        return HttpResponse("词不存在哦！")


@csrf_exempt
def sim_visualdu(request):#相似词查询
    a_title=request.POST.get("a_title")
    model_name = "{}.model".format(time.strftime("%Y-%m-%d",time.localtime())+a_title)
    model1='./static/model/'+model_name
    model=Word2Vec.load(model1)
    word=request.POST.get('word')
    try:
        sim=model.wv.most_similar(positive=[word], topn=5)
        data={'sim':sim}
        return JsonResponse(data)
    except:
        return HttpResponse("词不存在哦！")
@csrf_exempt   
def sim(request):#相似度查询
    a_title=request.POST.get("a_title")
    model_name = "{}.model".format(time.strftime("%Y-%m-%d",time.localtime())+a_title)
    model1='./static/model/'+model_name
    model=Word2Vec.load(model1)
    word1=request.POST.get('word1')
    word2=request.POST.get('word2')
    word_list=[]
    word_list.append(model.wv.index_to_key)
    sim1=model.wv.similarity(word1,word2)
    sim1=float(sim1)
    data={'sim1':sim1}
    return JsonResponse(data)