# encoding:utf-8
from django.db import models
from django.utils.timezone import now

from datetime import date

import uuid

# Create your models here.


class Author(models.Model):
    """
    作者对象
    """
    # 性别选择项
    CONFIDENTIALITY = 'CO'  # 保密
    MAN = 'MA'  # 男
    WOMAN = 'WO'  # 女
    GENDER_CHOICES = (
        (CONFIDENTIALITY, 'Confidentiality'),
        (MAN, 'Man'),
        (WOMAN, 'Woman'),
    )

    # uuid
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                            editable=False)
    # 昵称
    name = models.CharField(max_length=20, null=False, unique=True)
    # 密码create_time
    password = models.CharField(max_length=16)
    # 性别
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES,
                              default=CONFIDENTIALITY)
    # 生日
    birthday = models.DateTimeField(null=True)
    # 邮件地址
    email = models.EmailField(null=False, unique=True)

    # 注册时间
    create_time = models.DateTimeField(auto_now=now())

    def __str__(self):
        return self.name


class Comment(models.Model):
    """
    文章评论对象
    """
    pass


class Article(models.Model):
    """
    博客文章对象
    """
    # uuid
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                            editable=False)
    # 文章名称
    name = models.CharField(max_length=50, null=False)
    # 文章内容
    content = models.TextField(null=False)
    # 所属类别
    category = models.CharField(max_length=10, null=False)
    # 好评数
    praise = models.IntegerField(default=0)
    # 浏览量
    visits_num = models.IntegerField(default=-1)
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=now())
    # 状态
    status = models.BooleanField(default=True)
    # 外键：评论
    # comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    # 外键:作者
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.name

    def change_praise(self):
        """
        增加好评数方法
        :return:
        """
        self.praise += 1

        return {
            'status': True,
            'reason': None,
        }

    def change_visits_num(self):
        """
        增加浏览数量方法
        :return:
        """
        self.visits_num += 1

        return {
            'status': True,
            'reason': None,
        }


class Plan(models.Model):
    """
    网站计划任务对象
    """
    # 计划任务状态选项
    STATUS_CHOICES = (
        (-1, '进行中'),
        (0, '逾期'),
        (1, '已完成'),
        (2, '放弃'),
    )
    # 计划任务紧急程度选项
    EMERGENCY_CHOICES = (
        (0, '有空再做'),
        (1, '正常处理'),
        (2, '优先处理'),
        (3, '十万火急'),
    )
    # uuid
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                            editable=False)
    # 计划名称
    name = models.CharField(max_length=50, null=False)
    # 计划详细描述
    content = models.TextField(null=False)
    # 计划状态
    status = models.IntegerField(choices=STATUS_CHOICES, default=-1)
    # 紧急程度
    emergency_level = models.IntegerField(choices=EMERGENCY_CHOICES, default=1)
    # 制定计划时间
    planning_time = models.DateField(default=now)
    # 预计完成时间
    estimated_time = models.DateField(null=False)
    # 实际完成时间
    complete_time = models.DateField(null=True)
    # 原因
    reason = models.TextField(null=True)

    def give_up_plan(self):
        """
        放弃计划
        :return:
        """
        self.status = 2
        if self.reason == '逾期重启计划':
            self.reason = '逾期重启放弃计划'
        elif self.reason == '测试逾期 | 未重启':
            self.reason = '逾期放弃计划'
        else:
            self.reason = '放弃计划'

        return {
            'status': True,
            'reason': None,
        }

    def finish_plan(self):
        """
        完成计划
        :return:
        """
        now_time = date.today()

        if (self.estimated_time - now_time).days >= 15:
            if not self.reason == '逾期重启计划':
                self.reason = '超前完成'
        elif 15 > (self.estimated_time - now_time).days >= 7:
            if not self.reason == '逾期重启计划':
                self.reason = '提前完成'
        else:
            if not self.reason == '逾期重启计划':
                self.reason = '按时完成'

        self.status = 1
        self.complete_time = now_time

        return {
            'status': True,
            'reason': None,
        }
