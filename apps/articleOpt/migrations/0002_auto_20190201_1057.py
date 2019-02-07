# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articleOpt', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='user',
            field=models.ForeignKey(verbose_name='回复者', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='article',
            field=models.ForeignKey(verbose_name='评论所属文章', to='articleOpt.article'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(verbose_name='评论者', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='article',
            name='type',
            field=models.ForeignKey(verbose_name='所属类别', to='articleOpt.articleType'),
        ),
        migrations.AddField(
            model_name='article',
            name='user',
            field=models.ForeignKey(verbose_name='作者', to=settings.AUTH_USER_MODEL),
        ),
    ]
