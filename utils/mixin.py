from django.contrib.auth.decorators import login_required

#限制登录后才能访问的类
class LoginRequireMixin(object):
    @classmethod
    def as_view(cls,**initkwargs):
        #调用父类的as_view
        view = super(LoginRequireMixin,cls).as_view(**initkwargs)
        return login_required(view)