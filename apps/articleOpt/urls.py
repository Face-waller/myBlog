from django.conf.urls import url
from apps.articleOpt import views
from articleOpt.views import ArticleWriteView,ArticleRead,replyWrite,commentWrite

urlpatterns = [
    #通过url函数设置url路由配置项
    url(r'^articleRead/(?P<art_id>\d+)$', ArticleRead.as_view(), name='articleRead'),
    url(r'^articleWrite$', ArticleWriteView.as_view(), name='articleWrite'),
    url(r'^replyWrite', replyWrite.as_view(), name='replyWrite'),
    url(r'^commentWrite', commentWrite.as_view(), name='commentWrite'),
]