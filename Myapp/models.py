from django.db import models

# Create your models here.

class DB_project(models.Model):
    name = models.CharField(max_length=30,null=True,blank=True)
    creater = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return '项目名称' + self.name