from django.conf.urls import url
from apps.user import views
from user.views import RegisterView,ActiveView,LoginView,LogoutView

urlpatterns = [
    #通过url函数设置url路由配置项
    url(r'^register$',RegisterView.as_view(),name='register'),#注册
    url(r'^active/(?P<token>.*)$',ActiveView.as_view(),name='active'),#激活
    url(r'^login$',LoginView.as_view(),name='login'),#登录
    url(r'^logout$',LogoutView.as_view(),name='logout'),#登出
]