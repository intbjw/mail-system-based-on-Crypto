# Create your models here.
from django.db import models

# Create your models here.

# 数据库结构v1.0
class User(models.Model):

    gender = (
        ('male', "男"),
        ('female', "女"),
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default="男")
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"


class Sendemail(models.Model):
    '''
    发送箱：
        主题
        收件人
        发件人id
        邮件内容
        附件
        发送时间
        状态
    '''
    flag = (
        (1,'发送成功'),
        (0,'发送失败'),
    )
    subject = models.CharField(max_length=50)
    recipient = models.CharField(max_length=50)
    uid = models.IntegerField()
    letter = models.CharField(max_length=1000)
    affix = models.BinaryField()
    sendTime = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=flag)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ["-sendTime"]
        verbose_name = "发件箱"
        verbose_name_plural = "发件箱"


class Recipemail(models.Model):
    '''
        收件箱：
            id 自增
            主题
            收件人
            发件人
            邮件内容
            附件
            发送时间
            是否可读  0或1
    '''
    flag = (
        (1, '发送成功'),
        (0, '发送失败'),
    )
    subject = models.CharField(max_length=50)
    recipient = models.CharField(max_length=50)
    addresser = models.CharField(max_length=50)
    letter = models.CharField(max_length=1000)
    affix = models.BinaryField()
    sendTime = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField()

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ["-sendTime"]
        verbose_name = "收件箱"
        verbose_name_plural = "收件箱"


class adressbook(models.Model):
    '''
        联系表:
            用户名
            地址
            用户id
    '''
    username = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    uid = models.IntegerField()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "联系人"
        verbose_name_plural = "联系人"
