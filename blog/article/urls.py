"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    # 主页
    path('home/', views.home_view, name='home'),
    # 文章页面
    path('article/<uuid:uuid>/<int:num>/', views.get_article_view, name='article'),
    # 按类型查找文章功能
    path('category/<str:category>/', views.get_article_by_category_view, name='category'),
    # 按总类型查找所有子类型文章功能
    path('category_super/<str:category_super>/', views.get_article_super_category_view, name='category_super'),
    # 保存文章
    path('save_article/', views.save_article_view, name='save_article'),
    # 登录时接收客户端验证码功能
    path('save_code', views.save_login_code_view, name='save_code'),
    # 登录功能
    path('log_in/', views.log_in_view, name='log_in'),
    # 注销功能
    path('log_out/', views.log_out_view, name='log_out'),
    # 注册功能
    path('sign_up/', views.sign_up_view, name='sign_up'),
    # 注册时验证用户是否存在功能
    path('inspect_author/',views.inspect_author_view, name='inspect_author'),
    # 发送电子邮件验证码功能
    path('send_email/', views.send_email_code_view, name='send_email'),
    # 上传图片
    path('upload_image/', views.upload_image_view, name='upload_image'),
    # 适配简单页面，如访问welcome、login、registration等不需要传递参数及不需要返回值的页面
    path('<str:url>/', views.adaptive_view, name='adaptive'),
]
