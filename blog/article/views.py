# coding:utf-8

from django.shortcuts import render_to_response
import json

from django.http import HttpResponse

from . import models
# Create your views here.


def index(request):
    return render_to_response('welcome.html')


def home(request):
    artice = models.Article.objects.all()
    return render_to_response('home.html', {'article_list': list(artice)})


def save_article(request):
    if request.method == 'POST':
        article_dict = json.loads(request.body)
        models.Article.objects.create(name=article_dict['name'],
                                      content=article_dict['content'])
        return HttpResponse('保存成功！')


def get_article(request, name):
    print(name)
    if request.method == 'GET':
        artice = models.Article.objects.filter(name=name)
        name = artice[0].name
        content = artice[0].content
        return render_to_response('article.html', {'name': name, 'content': content})
