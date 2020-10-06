from django.shortcuts import render
from TestModel.models import Main,Mark

def kevenano(request):
    context = {}
    context['hello'] = 'Hello World!'
    context['bye'] = 'Bye Bye!'
    context['list'] = [0,1,2,3,4,5,6]
    context['dateDic'] = {'year':2020,'month':'oct','day':1}
    context['result'] = Main.objects.get(id=19).tags
    return render(request, 'kevenano.html', context)
