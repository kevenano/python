from django.shortcuts import render
from TestModel.models import Main
from django.http import HttpResponse,HttpResponseRedirect
import sys
from django.db.models import Q

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
        res = Main.objects.filter(*QList)[0:10]
        message['tags'] = tags
        message['result'] = res
        return render(request, 'index.html', message)
