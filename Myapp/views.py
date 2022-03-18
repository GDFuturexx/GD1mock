import json
import os
import random
import re
import shutil
import subprocess

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from Myapp.models import *


# Create your views here.
# 进入项目列表
@login_required
def project_list(request):
    project = DB_project.objects.all()
    buttons = [
        {"name": "新增项目", "href": "/add_project/", "icon": "calendar-plus-o"},
        {"name": "项目数据", "href": "javascript:project_data()", "icon": "database"}
    ]
    page_name = "项目列表页"
    return render(request, 'project_list.html', {"projects": project, "buttons": buttons, "page_name": page_name})


# 新增项目
def add_project(request):
    project = DB_project.objects.create(name='新项目', creater=request.user.username)
    shutil.copy('Myapp/mitm_edits/mitm_edit.py', f'Myapp/mitm_edits/{project.id}_mitm_edit.py')
    return HttpResponseRedirect('/project_list/')


# 删除项目
def del_project(request, pid):
    DB_project.objects.filter(id=pid).delete()
    DB_mock.objects.filter(project_id=pid).delete()
    try:
        os.remove(f'Myapp/mitm_edits/{pid}_mitm_edit.py')
    except:
        ...
    return HttpResponseRedirect('/project_list/')


# 保存项目
def save_project(request):
    new_name = request.GET['new_name']
    project_id = request.GET['project_id']
    DB_project.objects.filter(id=project_id).update(name=new_name)
    return HttpResponse('')


# 获取项目数据
def project_data(request):
    res = ''
    projects = DB_project.objects.all()
    for project in projects:
        res += '【' + str(project.id) + '】-'
        res += '【' + project.name + '】-'
        res += '【' + project.creater + '】-'

        # 单元数量
        res += '【' + str(len(DB_mock.objects.filter(project_id=project.id))) + '】-'

        res += '【' + str(project.run_counts) + '】-'
        res += '【' + str(project.mock_counts) + '】'
        res += '<br>'
    return HttpResponse(res)


# 进入登录注册页面
def login(request):
    return render(request, 'login.html')


# 登录
def sign_in(request):
    # 获取来自页面用户输入的用户名和密码
    username = request.POST['in_username']
    password = request.POST['in_password']
    # 去数据库用户表查询真假
    user = auth.authenticate(username=username, password=password)
    # 如果为假，不登录，重新返回登录注册页面
    if user is None:
        # return HttpResponse('密码错误')
        return HttpResponse('0')
    # 如果为真，登录，跳转到项目列表页
    else:
        auth.login(request, user)
        request.session['user'] = username
        return HttpResponse('1')


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
    code = str(random.randint(1000, 9999))
    # 保存验证码
    User.objects.filter(username=username).update(last_name=code)
    # 发送邮件
    # print(code)
    msg = '这是您找回密码的验证码：' + code
    send_mail('mock平台找回密码', msg, settings.EMAIL_FROM, [email])
    # 返回 yes
    return HttpResponse('yes')


# 进入 mock 列表页
def mock_list(request, project_id):
    res = {}
    # 从数据库拿出符合条件的 mock 列表
    res['mocks'] = DB_mock.objects.filter(project_id=project_id)
    # 根据项目 id 去数据库找出这个项目
    project = DB_project.objects.filter(id=project_id)[0]
    # 拿到当前平台ip
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    res['buttons'] = [
        {"name": "新增单元", "href": f"/add_mock/{project.id}/", "icon": "plus-square"},
        {"name": "抓包导入", "href": "", "icon": "cc"},
        {"name": "项目设置", "href": "javascript:project_set()", "icon": "gear"},
        {"name": "启动服务", "href": f"/server_on/{project_id}/", "icon": "check-square"},
        {"name": "关闭服务", "href": f"/server_off/{project_id}/", "icon": "window-close"},
    ]
    res['page_name'] = f'项目详情页：【{project.name}】' + '【host】：' + ip + '【port】：' + str(9000 + int(project_id))
    res['project_state'] = '服务状态：' + str(project.state)
    res['project_id'] = project_id
    return render(request, 'mock_list.html', res)


# 新增 mock 单元
def add_mock(request, project_id):
    DB_mock.objects.create(name='新单元', project_id=project_id)
    return HttpResponseRedirect(f'/mock_list/{project_id}/')


# 删除 mock 单元
def del_mock(request, mock_id):
    mocks = DB_mock.objects.filter(id=mock_id)
    project_id = mocks[0].project_id
    mocks.delete()
    return HttpResponseRedirect(f'/mock_list/{project_id}/')


# 保存mock单元
def save_mock(request):
    mock_id = request.GET['mock_id']
    mock_name = request.GET['mock_name']
    catch_url = request.GET['catch_url']
    mock_response_body = request.GET['mock_response_body']
    model = request.GET['model']
    response_headers = request.GET['response_headers']
    state_code = request.GET['state_code']
    mock_response_body_lj = request.GET['mock_response_body_lj']
    DB_mock.objects.filter(id=mock_id).update(name=mock_name,
                                              catch_url=catch_url,
                                              mock_response_body=mock_response_body,
                                              model=model,
                                              response_headers=response_headers,
                                              state_code=state_code,
                                              mock_response_body_lj=mock_response_body_lj,
                                              )
    return HttpResponse('')


# 获取 mock 单元的最新数据
def get_mock(request):
    mock_id = request.GET['mock_id']
    mock = DB_mock.objects.filter(id=mock_id).values()[0]
    res = {"mock": mock}
    return HttpResponse(json.dumps(res), content_type='application/json')


# 启用 mock 单元
def mock_on(request, mock_id):
    mock = DB_mock.objects.filter(id=mock_id)
    mock.update(state=True)
    project_id = mock[0].project_id
    return HttpResponseRedirect(f'/mock_list/{project_id}/')


# 弃用 mock 单元
def mock_off(request, mock_id):
    mock = DB_mock.objects.filter(id=mock_id)
    mock.update(state=False)
    project_id = mock[0].project_id
    return HttpResponseRedirect(f'/mock_list/{project_id}/')


# # 启动服务
# def server_on(request, project_id):
#     port = str(9000 + int(project_id))
#     script = 'Myapp/mitm_edits/' + project_id + '_mitm_edit.py'
#     cmd = f'mitmproxy -p {port} -s {script}'
#     subprocess.call(cmd, shell=True)
#     DB_project.objects.filter(id=project_id).update(state=True)
#     return HttpResponseRedirect(f'/mock_list/{project_id}/')


# 线程控制启动服务
def server_on(request, project_id):
    import threading
    def abc():
        port = str(9000 + int(project_id))
        script = 'Myapp/mitm_edits/' + project_id + '_mitm_edit.py'
        cmd = f'nohup mitmdump -p {port} -s {script}'
        subprocess.call(cmd, shell=True)

    t = threading.Thread(target=abc)
    t.start()
    DB_project.objects.filter(id=project_id).update(state=True)
    return HttpResponseRedirect(f'/mock_list/{project_id}/')


# 关闭服务
def server_off(request, project_id):
    port = str(9000 + int(project_id))

    # (macOS、Linux）
    # cmd = f'ps -ef|grep mitm |grep {port}'
    # res = subprocess.check_output(cmd, shell=True)

    # Windows
    res = subprocess.check_output('wmic process where caption="python.exe" get processid,commandline', shell=True)

    for i in str(res).split(r'\n'):
        if 'python.exe' in i:
            # if project_id + '_mitm_edit.py' in i:

            # (macOS、Linux）
            # pid = max([int(i) for i in re.findall(r'\d+', i.split('/')[0])])

            # Windows
            pid = max([int(i) for i in re.findall(r'\d+', i.split('\\')[-3])])

            # (macOS、Linux）
            # cmd2 = f'kill -9 {str(pid)}'
            # subprocess.check_output(cmd2, shell=True)

            # Windows
            subprocess.call(f'taskkill /T /F /PID {pid}', shell=True)

            print('进程已杀死！')
            break
    else:
        print('进程未找到！')
    DB_project.objects.filter(id=project_id).update(state=False)
    return HttpResponseRedirect(f'/mock_list/{project_id}/')
