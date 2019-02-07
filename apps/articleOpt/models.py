from django.db import models
from db.base_model import BaseModel
from DjangoUeditor.models import UEditorField
# Create your models here.

class articleType(BaseModel):
    '''文章类型模型类'''
    type = models.CharField(max_length=30,verbose_name='文章类型')
    class Meta:
        db_table = 'Blog_articleType'
        verbose_name = '文章类型'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.type

class article(BaseModel):
    '''文章模型类'''
    title = models.CharField(max_length=60, verbose_name='文章标题')
    descriptive = models.CharField(max_length=60, verbose_name='文章描述')
    #文章密码为用户密码
    is_secrete = models.BooleanField(default=False, verbose_name='是否加密')
    detail = UEditorField(verbose_name='文章内容')
    user = models.ForeignKey('user.User', verbose_name='作者')
    type = models.ForeignKey('articleType',verbose_name='所属类别')

    class Meta:
        db_table = 'Blog_article'
        verbose_name = '文章'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.title

class reply(BaseModel):
    '''回复模型类'''
    detail = models.CharField(max_length=500,verbose_name='回复内容')
    user = models.ForeignKey('user.User',verbose_name='回复者')
    comment = models.ForeignKey('comment',verbose_name='回复所属评论')

    class Meta:
        db_table = 'Blog_reply'
        verbose_name = '回复'
        verbose_name_plural = verbose_name
    def __str__(self):
        return str(self.id)

class comment(BaseModel):
    '''评论模型类'''
    detail = models.CharField(max_length=500,verbose_name='评论内容')
    user = models.ForeignKey('user.User',verbose_name='评论者')
    article = models.ForeignKey('article',verbose_name='评论所属文章')

    class Meta:
        db_table = 'Blog_comment'
        verbose_name = '评论'
        verbose_name_plural = verbose_name
    def __str__(self):
        return str(self.id)
