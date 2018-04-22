# coding:utf-8

from django.shortcuts import render_to_response
import json
import os
import uuid
import time

from django.http import HttpResponse, JsonResponse

from blog.settings import BASE_DIR

from . import models
# Create your views here.


def index(request):
    return render_to_response('welcome.html')


def home(request):
    artice = models.Article.objects.all()
    return render_to_response('home.html', {'article_list': list(artice)})


def save_article(request):
    if request.method == 'POST':
        print(request.body)
        article_dict = json.loads(request.body)
        models.Article.objects.create(name=article_dict['name'],
                                      content=article_dict['content'])
        data = {
            'result': 'ok',
        }
        return JsonResponse(data)


def get_article(request, uuid):
    print(uuid)
    if request.method == 'GET':
        artice = models.Article.objects.get(uuid=uuid)
        name = artice.name
        content = artice.content
        return render_to_response('article.html', {'name': name, 'content': content})


def edit_article(request):
    if request.method == 'GET':
        return render_to_response('edit_article.html')


def test_html(request):
    if request.method == 'GET':
        return render_to_response('test.html')


def save_image(request):
    if request.method == 'POST':
        # 获取文件对象
        image = request.FILES.get('image')

        # 生成唯一的图片名
        image_name = '{0}.{1}'.format(uuid.uuid4(), image.name.split('.')[-1])

        # 保存图片
        path = os.path.join('static', 'images', 'markdown', image_name)
        with open(os.path.join(BASE_DIR, path), 'wb+') as f:
            for chunk in image.chunks():
                f.write(chunk)

        data = {
            'result': 'ok',
            'path': 'http://127.0.0.1:8000/{0}'.format(path)
        }

        time.sleep(2)

        return JsonResponse(data)

