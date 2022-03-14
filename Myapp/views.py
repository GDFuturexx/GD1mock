from django.shortcuts import render,HttpResponseRedirect
from Myapp.models import *

# Create your views here.
# 进入项目列表
def project_list(request):
    project = DB_project.objects.all()
    return render(request, 'project_list.html', {"projects": project})

# 删除项目
def del_project(request, pid):
    # print(pid)
    DB_project.objects.filter(id=pid).delete()
    return HttpResponseRedirect('/project_list/')