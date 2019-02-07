# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import DjangoUeditor.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('title', models.CharField(verbose_name='文章标题', max_length=60)),
                ('descriptive', models.CharField(verbose_name='文章描述', max_length=60)),
                ('is_secrete', models.BooleanField(verbose_name='是否加密', default=False)),
                ('detail', DjangoUeditor.models.UEditorField(verbose_name='文章内容')),
            ],
            options={
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
                'db_table': 'Blog_article',
            },
        ),
        migrations.CreateModel(
            name='articleType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('type', models.CharField(verbose_name='文章类型', max_length=30)),
            ],
            options={
                'verbose_name': '文章类型',
                'verbose_name_plural': '文章类型',
                'db_table': 'Blog_articleType',
            },
        ),
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('detail', models.CharField(verbose_name='评论内容', max_length=500)),
            ],
            options={
                'verbose_name': '评论',
                'verbose_name_plural': '评论',
                'db_table': 'Blog_comment',
            },
        ),
        migrations.CreateModel(
            name='reply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('detail', models.CharField(verbose_name='回复内容', max_length=500)),
                ('comment', models.ForeignKey(verbose_name='回复所属评论', to='articleOpt.comment')),
            ],
            options={
                'verbose_name': '回复',
                'verbose_name_plural': '回复',
                'db_table': 'Blog_reply',
            },
        ),
    ]
