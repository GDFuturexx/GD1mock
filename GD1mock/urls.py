"""GD1mock URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,re_path
from Myapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('project_list/', project_list),  # 项目列表页
    re_path('del_project/(?P<pid>.+)/', del_project),  # 删除项目
    path('login/', login),  # 登录注册页面
    path('logout/', logout),  # 注销退出登录页面
    path('accounts/login/', login),  # 当没有登录态的时候访问的登录注册页面
    path('sign_in/', sign_in),  # 登录动作
    path('sign_up/', sign_up),  # 注册动作
]
