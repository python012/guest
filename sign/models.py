from django.db import models

# Create your models here.

# One modal, one Python class, one table in database
# model创建好后，需要执行数据库迁移 
# 1. python3 manage.py makemigrations sign
# 2. python3 manage.py migrate

# 发布会表
class Event(models.Model):
    """
    model for the Press Conference
    """
    name = models.CharField(max_length=100)             # 发布会标题
    limit = models.IntegerField()                       # 参加人数
    status = models.BooleanField()                      # 状态
    address = models.CharField(max_length=200)          # 地址
    start_time = models.DateTimeField('events time')    # 发布会开始时间
    create_time = models.DateTimeField(auto_now=True)   # 创建时间，自动获取当前时间

    def __str__(self):
        return self.name

# 嘉宾表
class Guest(models.Model):
    """
    model for the guest
    """
    event = models.ForeignKey(Event)                   # 关联发布会id
    realname = models.CharField(max_length=64)         # 姓名
    phone = models.CharField(max_length=16)            # 手机号
    email = models.EmailField()                        # 电子邮箱
    sign = models.BooleanField()                       # 签到状态
    create_time = models.DateTimeField(auto_now=True)  # 创建时间，自动获取当前时间

    class Meta:
        unique_together = ("event", "phone")           # 设置2个字段为联合主键

    def __str__(self):
        return self.realname
