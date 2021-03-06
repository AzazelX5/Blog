# Generated by Django 2.0.4 on 2018-05-21 19:42

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_article_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('status', models.IntegerField(choices=[(-1, '未完成'), (0, '逾期'), (1, '已完成'), (2, '放弃')], default=-1)),
                ('planning_time', models.DateField(default=datetime.datetime(2018, 5, 21, 19, 42, 32, 837675))),
                ('estimated_time', models.DateField()),
                ('complete_time', models.DateField(null=True)),
                ('reason', models.TextField(null=True)),
            ],
        ),
    ]
