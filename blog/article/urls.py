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
    path('welcome/', views.index),
    path('home/', views.home, name='home'),
    path('save/', views.save_article, name='save'),
    path('get/<uuid:uuid>/', views.get_article, name='get'),
    path('article/', views._get_article, name='article'),
    path('edit/', views.edit_article, name='edit'),
    path('login/', views.login_html, name='login'),
    path('save_image/', views.save_image, name='save_image'),
    path('log_in/', views.log_in, name='log_in'),
    path('registration/', views.registration, name='registration'),
    path('registration_page/', views.registration_html, name='registration_page')
]
