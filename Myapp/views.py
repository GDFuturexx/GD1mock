import random
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render,HttpResponseRedirect
from Myapp.models import *

# Create your views here.
# 进入项目列表
@login_required
def project_list(request):
    project = DB_project.objects.all()
    return render(request, 'project_list.html', {"projects": project})

# 删除项目
def del_project(request, pid):
    # print(pid)
    DB_project.objects.filter(id=pid).delete()
    return HttpResponseRedirect('/project_list/')

# 进入登录注册页面
def login(request):
    return render(request, 'login.html')

# 登录
def sign_in(request):
    # 获取来自页面用户输入的用户名和密码
    username = request.GET['in_username']
    password = request.GET['in_password']
    # 去数据库用户表查询真假
    user = auth.authenticate(username=username, password=password)
    # 如果为假，不登录，重新返回登录注册页面
    if user is None:
        return HttpResponseRedirect('/login/')
    # 如果为真，登录，跳转到项目列表页
    else:
        auth.login(request, user)
        request.session['user'] = username
        return HttpResponseRedirect('/project_list/')

# 注销退出登录
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')

# 注册
def sign_up(request):
    # 获取用户名、密码、邮箱
    username = request.GET['up_username']
    password = request.GET['up_password']
    email = request.GET['up_email']
    # 注册
    try:
        # 注册成功
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        auth.login(request, user)
        request.session['user'] = username
        return HttpResponseRedirect('/project_list/')
    except:
        # 注册失败
        return HttpResponseRedirect('/login/')

# 重设密码
def reset_password(request):
    # 获取用户名,验证码，新密码
    username = request.GET['fg_username']
    code = request.GET['fg_code']
    password = request.GET['fg_password']
    # 判断验证码
    check_code = User.objects.filter(username=username)[0].last_name
    if code == check_code:
        User.objects.filter(username=username).update(password=make_password(password))
        return HttpResponseRedirect('/login/')
    else:
        return HttpResponse('Verification code is not correct !')

# 发送验证码邮件
def send_email_pwd(request):
    # 获取用户名
    username = request.GET['username']
    # 根据用户名去数据库用户表获取对应邮箱
    email = User.objects.filter(username=username)[0].email
    # 生成随机验证码
    code = str(random.randint(1000,9999))
    # 保存验证码
    User.objects.filter(username=username).update(last_name=code)
    # 发送邮件
    # print(code)
    msg = '这是您找回密码的验证码：' + code
    send_mail('mock平台找回密码', msg, settings.EMAIL_FROM, [email])
    # 返回 yes
    return HttpResponse('yes')