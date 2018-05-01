# coding:utf-8
import json
import os
import uuid
import time

from random import Random

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives

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
            'path': 'http://10.0.0.105:8000/{0}'.format(path)
        }

        time.sleep(1)

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


def save_login_code_view(request):
    """
    将登陆时前端生成的验证码保存在session中，用来判断后面登录时是否是通过正常途径登录的。
    :param request:
    :return:
    """
    if request.method == 'GET':
        code = request.GET.get('code')
        print(code)
        request.session['login_code'] = code

        result = {
            "status": True,
            "reason": "保存成功！",
        }

        return JsonResponse(result)


def log_in_view(request):
    """
    登录功能视图
    :param request:
    :return:
    """
    if request.method == 'POST':
        author_dict = json.loads(request.body)
        # 判断验证码，防止非正常途径登录。
        if request.session['login_code'] == author_dict['code']:
            author = models.Author.objects.filter(
                name__exact=author_dict['name'],
                password__exact=author_dict['password'],
            ).first()

            if author:
                request.session['name'] = author.name
                # 判断是否勾选记住密码，是则保存session一个月，否则关闭浏览器立即失效
                if author_dict['keep_pass']:
                    request.session.set_expiry(2592000)
                else:
                    request.session.set_expiry(0)

                status = True
                reason = "登录成功！"
            else:
                status = False
                reason = "账号或密码输入有误！"
        else:
            status = False
            reason = "验证码不正确，不是正常的访问，拒绝登录。。。"

        result = {
            "status": status,
            "reason": reason,
        }
        return JsonResponse(result)


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
            "reason": "注销成功，3S后跳转到主页。。。",
            "url": "/blog/home/",
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
        print(request.POST)
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
        del request.session['sign_up_code']

        result = {
            "status": True,
            "reason": "注册成功，3S后跳转到登录页面。。。",
            "url": 'http://test.ngroktest.nodes.studio/blog/login/',
        }
        return render(request, 'prompt.html', {'result': result})


def inspect_author_view(request):
    """
    注册 时 验证账号、邮箱、以及验证码等视图
    :param request:
    :return:
    """
    if request.method == 'GET':
        if request.GET.get('type') == 'name':
            name = request.GET.get('value')
            try:
                models.Author.objects.get(name__exact=name)
                status = False
                reason = '该账号已被注册！'
            except ObjectDoesNotExist:
                status = True
                reason = '该账号可以使用！'
        elif request.GET.get('type') == 'email':
            email = request.GET.get('value')
            try:
                models.Author.objects.get(email__exact=email)
                status = False
                reason = '该邮箱已经注册！'
            except ObjectDoesNotExist:
                status = True
                reason = '该邮箱可以使用！'
        else:
            code = request.GET.get('value')
            try:
                r_str = request.session['sign_up_code']
                print(r_str)
                if code == r_str:
                    status = True
                    reason = '验证码输入正确！'
                else:
                    status = False
                    reason = '验证码输入有误！'
            except KeyError:
                status = False
                reason = '验证码过期！'
        result = {
            "status": status,
            "reason": reason,
        }
        return JsonResponse(result)


def send_email_code_view(request):
    """
    注册时给指定邮箱发送验证码视图
    :param request:
    :return:
    """
    if request.method == "POST":
        email_address = json.loads(request.body)['email']

        # 6位验证码
        r_str = random_str(6)
        # 将验证码存入session
        request.session['sign_up_code'] = r_str
        # 设置过期时间为5分钟
        request.session.set_expiry(30)

        # print("\n开始发送电子邮件， 目标邮箱：{0} , 验证码：{1}".format(email_address, r_str))
        # time_start = time.time()
        #
        # subject, from_email, to_email = \
        #     '[Azazel`s Blog] 注册验证码', 'azazel_zhao@163.com', 'azazel.zhao@live.cn'
        #
        # text_content = '首先，感谢你在我的博客注册！\n下面是验证码：{0} \n此验证吗在5分钟内有效，请抓紧时间注册！\n欢迎你的加入！'.format(r_str)
        #
        # html_content = '<h2>首先，感谢你在我的博客注册！</h2></ br>' \
        #                '<p>下面是验证码：</p> <strong>{0}</strong> </ br>' \
        #                '<h3>此验证吗在5分钟内有效，请抓紧时间注册！</h3></ br>' \
        #                '<h3>欢迎你的加入！</h3>'.format(r_str)
        #
        # msg = EmailMultiAlternatives(subject, text_content,
        #                              from_email, [to_email])
        # msg.attach_alternative(html_content, "text/html")
        # msg.send()
        #
        # time_end = time.time()
        # print("邮件发送成功，用时：{0} s\n".format(time_end-time_start))
        data = {
            'result': "测试版本，验证码为：{0}, 30S内有效".format(r_str),
        }
        return JsonResponse(data)


def random_str(random_length=8):
    """
    生成指定位数的随机数
    :param random_length: 需要生成随机数的长度
    :return:
    """
    r_str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    random = Random()
    for i in range(random_length):
        r_str += chars[random.randint(0, len(chars) - 1)]

    return r_str
