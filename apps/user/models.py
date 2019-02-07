from django.db import models
from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# Create your models here.

class User(AbstractUser,BaseModel):
    '''用户模型类'''

    def generate_active_token(self):
        '''生成用户签名字符串'''
        serializer = Serializer(settings.SECRET_KEY,3600)
        info = {'confirm':self.id}
        token = serializer.dump(info)
        return token.decode()
    class Meta:
        db_table = 'Blog_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

