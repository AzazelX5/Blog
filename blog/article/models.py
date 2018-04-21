# encoding:utf-8
from django.db import models
from django.utils.timezone import now

import uuid

# Create your models here.


class Article(models.Model):
    """
    博客文章对象
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,
                            editable=False)
    name = models.CharField(max_length=50)
    content = models.TextField(null=True)
    create_time = models.DateTimeField(null=True, auto_now=now())

    def __str__(self):
        return self.name
