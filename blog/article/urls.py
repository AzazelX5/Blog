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
from django.urls import path, re_path
from . import views

urlpatterns = [
    # 主页
    path('home/', views.home_view, name='home'),
    # 文章页面
    path('article/<uuid:uuid>/', views.get_article_view, name='article'),
    # 保存文章
    path('save_article/', views.save_article_view, name='save_article'),
    # 登录功能
    path('log_in/', views.log_in_view, name='log_in'),
    # 注销功能
    path('log_out/', views.log_out_view, name='log_out'),
    # 注册功能
    path('sign_up/', views.sign_up_view, name='sign_up'),
    # 上传图片
    path('upload_image/', views.upload_image_view, name='upload_image'),
    # 适配简单页面，如访问welcome、login、registration等不需要传递参数的页面
    path('<str:url>/', views.adaptive_view, name='adaptive'),
]
