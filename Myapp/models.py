from django.db import models


# Create your models here.

class DB_project(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True)
    creater = models.CharField(max_length=30, null=True, blank=True)
    run_counts = models.IntegerField(default=0)
    mock_counts = models.IntegerField(default=0)
    state = models.BooleanField(default=False)  # 服务状态

    def __str__(self):
        return '项目名称' + self.name


class DB_mock(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True)
    state = models.BooleanField(default=False)
    project_id = models.CharField(max_length=30, null=True, blank=True)
    catch_url = models.CharField(max_length=500, null=True, blank=True)
    mock_response_body = models.TextField(null=True, blank=True)
    model = models.CharField(max_length=30,null=True,blank=True,default='fx')  # 拦截：lj,放行：fx
    response_headers = models.CharField(max_length=500,null=True,blank=True,default='{}')
    state_code = models.IntegerField(default=200)
    mock_response_body_lj = models.TextField(null=True,blank=True,default='')  # 拦截模式的写死的返回值

    def __str__(self):
        return self.name
