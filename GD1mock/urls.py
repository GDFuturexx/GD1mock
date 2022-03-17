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
from django.urls import path, re_path
from Myapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('project_list/', project_list),  # 项目列表页
    path('add_project/', add_project),  # 新增项目
    path('save_project/', save_project),  # 保存项目
    path('project_data/', project_data),  # 获取项目数据
    re_path('del_project/(?P<pid>.+)/', del_project),  # 删除项目
    path('login/', login),  # 登录注册页面
    path('logout/', logout),  # 注销退出登录页面
    path('accounts/login/', login),  # 当没有登录态的时候访问的登录注册页面
    path('sign_in/', sign_in),  # 登录动作
    path('sign_up/', sign_up),  # 注册动作
    path('reset_password/', reset_password),  # 重设密码
    path('send_email_pwd/', send_email_pwd),  # 发送验证码邮件
    re_path('mock_list/(?P<project_id>.+)/', mock_list),  # 项目列表页（mock 列表页）
    re_path('add_mock/(?P<project_id>.+)/', add_mock),  # 新增 mock 单元
    re_path('del_mock/(?P<mock_id>.+)/', del_mock),  # 删除 mock 单元
    path('save_mock/', save_mock),  # 保存单元
    path('get_mock/', get_mock),  # 获取 mock 单元的最新数据
    re_path('mock_on/(?P<mock_id>.+)/', mock_on),  # 启用 mock 单元
    re_path('mock_off/(?P<mock_id>.+)/', mock_off),  # 弃用 mock 单元
    re_path('server_on/(?P<project_id>.+)/', server_on),  # 启动服务
    re_path('server_off/(?P<project_id>.+)/', server_off),  # 关闭服务
]
