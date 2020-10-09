from django.shortcuts import render
from TestModel.models import Main
from django.http import HttpResponse, HttpResponseRedirect
import sys
from django.db.models import Q
from pprint import pprint
from django.views.decorators import csrf
import copy


# 测试页
def kevenano(request):
    context = {}
    context['hello'] = 'Hello World!'
    context['bye'] = 'Bye Bye!'
    context['list'] = [0, 1, 2, 3, 4, 5, 6]
    context['dateDic'] = {'year': 2020, 'month': 'oct', 'day': 1}
    context['result'] = Main.objects.get(id=19).tags
    return render(request, 'kevenano.html', context)


# 欢迎页
def welcome(request):
    return render(request, 'welcome.html')


# 在欢迎页搜索 get方法提交表单进入索引页
def welcomeSearch(request):
    request.encoding = 'UTF-8'
    message = {}
    if 'tags' in request.GET:
        # ##################处理tags################## #
        tags = request.GET['tags']
        tags = tags.split(",")
        QList = []
        for tag in tags:
            if tag != " ":
                if tag.startswith(r"~"):
                    QList.append(~Q(tags__contains=tag))
                else:
                    QList.append(Q(tags__contains=tag))
        # ##################处理tags################## #
        # print('########################################')
        # print(type(QList))
        # print(QList)
        # print(tags)
        res = Main.objects.filter(*QList)[0:100]
        message['tags'] = tags
        message['result'] = res
        return render(request, 'index.html', message)


# index页检索 post方法实现表单数据提交
def indexSearch(request):
    print('---------------###---------------')
    request.encoding = 'UTF-8'
    inData = {}
    formData = {}
    # 设置默认参数
    formData['ID_start'] = 1
    formData['ID_end'] = 999999
    formData['order'] = 'id'
    formData['rating_s'] = False
    formData['rating_q'] = False
    formData['rating_e'] = False
    formData['tags_input'] = ' '
    if request.POST:
        inData = request.POST
        pprint(inData)
    print('---------------###---------------')
    for k, v in inData.items():
        if k=='ID_start' or k=='ID_end':
            formData[k] = int(v)
        else:
            formData[k] = v
    pprint(formData)
    print('---------------###---------------')
    # 表单数据预处理
    if formData['ID_start'] < 1:
        formData['ID_start'] = 1
    if formData['ID_end'] < formData['ID_start']:
        t = formData['ID_end']
        formData['ID_end'] = formData['ID_start']
        formData['ID_start'] = t
    # 处理tags 构造查询参数列表
    tags = formData['tags_input']
    tags = tags.split(",")
    QList = []
    for tag in tags:
        if tag != " ":
            if tag.startswith(r"~"):
                QList.append(~Q(tags__contains=tag))
            else:
                QList.append(Q(tags__contains=tag))
    # ID范围部分
    QList.append(Q(id__range=(formData['ID_start'], formData['ID_end'])))
    # rating部分
    ratList = []
    if formData['rating_s']:
        ratList.append('s')
    if formData['rating_q']:
        ratList.append('q')
    if formData['rating_e']:
        ratList.append('e')
    QList.append(Q(rating__in=ratList))
    # mark部分
    QList.append(~Q(mark2__deleted='true'))
    pprint(QList)
    print('---------------###---------------')
    res = Main.objects.filter(*QList).order_by(formData['order'])[0:10]
    resDic = {}
    resLis = []
    for item in res:
        resDic['id'] = item.id
        resDic['score'] = item.score
        resLis.append(copy.copy(resDic))
    return render(request, 'index.html', {'preShow':resLis})
