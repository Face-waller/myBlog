from django.conf.urls import url
from content.views import Index,About,log,type_article,static_index

urlpatterns = [
    #通过url函数设置url路由配置项
    url(r'^static_index$',static_index.as_view(),name='static_index'),
    url(r'^about$',About.as_view(),name='about'),
    url(r'^log/(?P<page_num>\d+)$',log.as_view(),name='log'),
    url(r'^type_article/(?P<artype_id>\d+)/(?P<page_num>\d+)$',type_article.as_view(),name='type_article'),
    url(r'^',Index.as_view(),name='index'),

]

