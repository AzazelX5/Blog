# encoding:utf-8
from django.db import models
from django.utils.timezone import now

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
    content = models.TextField(null=False,)
    # 所属类别
    category = models.CharField(max_length=10, null=False)
    # 好评数
    praise = models.IntegerField(default=0)
    # 浏览量
    visits_num = models.IntegerField(default=-1)
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=now())
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
