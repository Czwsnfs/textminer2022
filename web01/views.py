from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import time
import xlwt
import json
import jieba
import jieba.posseg


# Create your views here.
def index(request):
    return render(request, "index.html")


@csrf_exempt
def read_file(request):
    # print('文件上传成功!')
    receive_file = request.FILES.get('file', None)
    filename = str(time.time()) + '.' + receive_file.name.split('.').pop()
    des = open('./static/test/'+filename, 'wb+')
    for line in receive_file.chunks():
        des.write(line)
    des.seek(0)
    content = {}
    content['text'] = des.read().decode()
    return JsonResponse(content)


@csrf_exempt
def to_dir(request):
    data = json.loads(request.body.decode())
    # print(json.loads(request.body.decode()))
    text = data['text']
    diy_list = data['diy']
    print("text':"+text)
    print("diy_list:")
    print(diy_list)
    for i in diy_list:
        print(i)
        jieba.add_word(i['word'], tag=i['flag'])
    # 这里存放后端代码
    seg_list = jieba.posseg.cut(text)
    # for i in diy_list:
    #     jieba.del_word(i['word'])
    jieba.del_word('*')
    content1 = {'word': [], 'flag': []}
    # new_data = {
    #     'word': ['一', '二', '三'],
    #     'flag': ['n', 'v', 'adv'],
    # }
    for word, flag in seg_list:
        content1['word'].append(word)
        content1['flag'].append(flag)
    print("content:")
    print(content1)
    return JsonResponse(content1)


@csrf_exempt
def save_excel(request):
    # print(request.body)
    # print(request.POST)
    print(json.loads(request.body.decode()))
    content = json.loads(request.body.decode())["list"]
    print("接收到的参数是：", content)
    wordbook = xlwt.Workbook(encoding='utf8')
    sheet = wordbook.add_sheet('sheet1')
    sheet.write(0, 0, '词语')
    sheet.write(0, 1, '词性')
    for i in range(len(content)):
        sheet.write(content[i]['key']+1, 0, content[i]['word'])
        sheet.write(content[i]['key']+1, 1, content[i]['flag'])
    time_str = str(time.time()).replace('.', '')
    # wordbook.save(os.path.abspath(os.path.dirname(os.getcwd())).replace('\\', '/')+'/textminer/static/wa_excel/' + time_str + '.xls')
    wordbook.save(r'G:/项目/textminer/public/group1/wordanaly/'+time_str+'.xls')
    return HttpResponse(time_str + '.xls')


@csrf_exempt
def test(request):
    return HttpResponse('1')