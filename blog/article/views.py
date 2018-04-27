# coding:utf-8

from django.shortcuts import render
import json
import os
import uuid
import time

from django.http import HttpResponse, JsonResponse

from blog.settings import BASE_DIR

from . import models
# Create your views here.


def adaptive_view(request, url):
    """
    适配简单页面视图
    :param request:
    :param url: 页面url前缀
    :return:
    """
    if request.method == 'GET':
        url_str = '{0}.html'
        print(url)
        return render(request, url_str.format(url))


def home_view(request):
    """
    主页视图
    :param request:
    :return:
    # """
    # if request.session.get('name'):
    #     del request.session['name']
    # else:
    #     request.session['name'] = 'Azazel'
    article_list = models.Article.objects.order_by("-create_time")

    return render(request, 'home.html', {'article_list': list(article_list)})


def get_article_view(request, uuid):
    """
    展示文章页面视图
    :param request:
    :param uuid: 文章uuid
    :return:
    """
    if request.method == 'GET':
        article = models.Article.objects.get(uuid=uuid)

        return render(request, 'article.html', {'article': article})


def upload_image_view(request):
    """
    上传图片视图
    :param request:
    :return:
    """
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
            'path': 'http://0.0.0.0:8000/{0}'.format(path)
        }

        time.sleep(2)

        return JsonResponse(data)


def save_article_view(request):
    """
    发表文章视图
    :param request:
    :return:
    """
    if request.method == 'POST':
        print(request.body)
        article_dict = json.loads(request.body)
        author = models.Author.objects.get(name='Azazel')
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


def log_in_view(request):
    """
    登录功能视图
    :param request:
    :return:
    """
    if request.method == 'POST':
        user = request.POST['user']
        password = request.POST['password']
        print(request.POST)
        print(request.POST['user'])
        author = models.Author.objects.filter(
            name=user,
            password=password,
        ).first()

        if author:
            request.session['name'] = author.name
            status = True
            reason = "登录成功"
        else:
            status = False
            reason = "账号或密码输入有误"

        result = {
            "status": status,
            "reason": reason,
        }
        return render(request, 'prompt.html', {'result': result})


def log_out_view(request):
    """
    注销功能视图
    :param request:
    :return:
    """
    if request.method == 'GET':
        del request.session['name']

        result = {
            "status": True,
            "reason": "注销成功",
        }
        return render(request, 'prompt.html', {'result': result})


def sign_up_view(request):
    """
    注册功能视图
    :param request:
    :return:
    """
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
        request.session['name'] = author.name
        result = {
            "status": True,
            "reason": "注册成功",

        }
        return render(request, 'prompt.html', {'result': result})
