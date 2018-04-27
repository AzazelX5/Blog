# coding:utf-8

from django.shortcuts import render_to_response, render
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
    if request.session.get('name'):
        del request.session['name']
    else:
        request.session['name'] = 'Azazel'
    artice = models.Article.objects.order_by("-create_time")
    return render(request, 'home.html', {'article_list': list(artice)})


def save_article(request):
    if request.method == 'POST':
        print(request.body)
        article_dict = json.loads(request.body)
        author  = models.Author.objects.get(name='Azazel')
        article = models.Article.objects.create(
            name=article_dict['name'],
            content=article_dict['content'],
            category="Python",
            author=author,
        )
        data = {
            'result': 'ok',
            'uuid': article.uuid,
        }
        return JsonResponse(data)


def get_article(request, uuid):
    print(uuid)
    if request.method == 'GET':
        artice = models.Article.objects.get(uuid=uuid)
        name = artice.name
        content = artice.content
        return render_to_response('article.html', {'name': name, 'content': content})


def _get_article(request):
    print(11111)
    if request.method == 'GET':
        uuid = request.GET.get('uuid')
        artice = models.Article.objects.get(uuid=uuid)
        name = artice.name
        content = artice.content
        return render_to_response('article.html',
                                  {'name': name, 'content': content})


def edit_article(request):
    if request.method == 'GET':
        return render_to_response('edit_article.html')


def login_html(request):
    if request.method == 'GET':
        return render_to_response('log_in.html')


def registration_html(request):
    if request.method == 'GET':
        return render_to_response('registration.html')


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
            'path': 'http://frptest.nodes.studio:8080//{0}'.format(path)
        }

        time.sleep(2)

        return JsonResponse(data)


def log_in(request):
    if request.method == 'POST':
        user = request.POST['user']
        password = request.POST['password']
        print(request.POST)
        print(request.POST['user'])
        author = models.Author.objects.filter(
            name=user,
            password=password,
        ).first()

        # if password == author.password:
        #     status = True
        #     reason = "登录成功"
        # else:
        #     status = False
        #     reason = "密码不正确"

        if author:
            request.session['name'] = author.name
            status = True
            reason = "登录成功"
        else:
            status = False
            reason = "密码不正确"

        result = {
            "status": status,
            "reason": reason,

        }
        return render_to_response('prompt.html', {'result': result})


def registration(request):
    if request.method == 'POST':
        email_str = '{0}@{1}'

        name = request.POST['user']
        password = request.POST['password']
        email = request.POST['email']

        if not request.POST['email_suffix'].strip():
            email_suffix = request.POST['email_default_suffix']
        else:
            email_suffix = request.POST['email_suffix']

        email = email_str.format(email, email_suffix)

        author = models.Author.objects.create(
            name=name,
            password=password,
            email=email
        )
        print(author)
        result = {
            "status": True,
            "reason": "注册成功",

        }
        return render_to_response('prompt.html', {'result': result})
