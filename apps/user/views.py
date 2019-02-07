from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from user.models import User
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired
from django.conf import settings
from celery_tasks.tasks import send_register_active_email
from django.contrib.auth import authenticate,login,logout
import re
# Create your views here.

#/user/register
class RegisterView(View):
    '''注册'''
    def get(self,request):
        '''显示注册页面'''
        return render(request,'user/register.html')

    def post(self,request):
        '''进行注册处理'''
        # 接收数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        aginpassword = request.POST.get('ag_pwd')
        email = request.POST.get('email')

        #校验数据合法性
        if len(username) != 6 or len(password) != 6:
            #长度不合法
            return render(request, 'user/register.html', {'errmsg': '您的用户名或密码长度不合法!'})
        try:
            for u in username:
                if (ord(str(u)) < 48) or (ord(str(u)) > 57 and ord(str(u)) < 65) or (ord(str(u)) > 90 and ord(str(u)) < 97) or (ord(str(u)) > 122):
                    return render(request, 'user/register.html', {'errmsg': '您输入的用户名不合法!'})
        except:
            return render(request, 'user/register.html', {'errmsg': '您输入的用户名不合法!'})

        try:
            for p in str(password):
                if (int(p) < 48) or (int(p) > 57):
                    return render(request, 'user/register.html', {'errmsg': '您输入的密码不合法!'})
        except:
            return render(request, 'user/register.html', {'errmsg': '您输入的密码不合法!'})


        # 进行数据校验
        if not all([username, password, aginpassword, email]):
            # 数据不完整
            return render(request, 'user/register.html', {'errmsg': '数据不完整!'})

        # 校验密码
        if password != aginpassword:
            return render(request, 'user/register.html', {'errmsg': '您输入的两次密码不一致!'})

        # 校验邮箱
        if not re.match('^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
            return render(request, 'user/register.html', {'errmsg': '您输入的邮箱格式不正确!'})

        # 校验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user:
            # 用户名已存在
            return render(request, 'user/register.html', {'errmsg': '您注册的用户名已存在!'})

        # 进行业务处理: 使用django内置方法进行用户注册
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()

        #发送激活邮件
        #激活链接中需要包含用户的身份信息,并且要把身份信息进行加密

        #加密用户的身份信息,生成激活token
        serializer = Serializer(settings.SECRET_KEY,3600)
        info = {'confirm':user.id}
        token = serializer.dumps(info)
        token = token.decode()
        #发邮件
        send_register_active_email.delay(email,username,token)

        # 返回应答
        return redirect(reverse('con_index:index'))

class ActiveView(View):
    '''用户账号激活'''
    def get(self,request,token):
        '''进行用户激活'''
        #解密获取要激活的用户信息
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            #获取待激活用户id
            user_id = info['confirm']
            #根据id获取用户信息
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()
            #跳转到登录页面
            return redirect(reverse('user:register'))
        except SignatureExpired as e:
            #激活链接已过期
            return HttpResponse('您的激活链接已过期!')

#/user/login
class LoginView(View):
    '''登录'''
    def get(self,request):
        '''显示登录页面'''
        #判断是否记住用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''
        context = {
            'username':username,
            'checked':checked,
        }
        return render(request,'user/login.html',context)

    def post(self,request):
        '''进行登录处理'''
        #接收数据
        username = request.POST.get('username')
        password = request.POST.get('password')
        #登录校验
        if not all([username,password]):
            return render(request,'user/login.html',{'errmsg':'您填写的不完整!'})

        #校验数据合法性
        if len(username) != 6 or len(password) != 6:
            #长度不合法
            return render(request, 'user/login.html', {'errmsg': '您输入的用户名或密码长度不合法!'})
        try:
            for u in username:
                if (ord(str(u)) < 48) or (ord(str(u)) > 57 and ord(str(u)) < 65) or (ord(str(u)) > 90 and ord(str(u)) < 97) or (ord(str(u)) > 122):
                    return render(request, 'user/login.html', {'errmsg': '您输入的用户名不合法!'})
        except:
            return render(request, 'user/login.html', {'errmsg': '您输入的用户名不合法!'})

        try:
            for p in str(password):
                if (ord(p) < 48) or (ord(p) > 57):
                    return render(request, 'user/login.html', {'errmsg': '您输入的密码不合法!'})
        except:
            return render(request, 'user/login.html', {'errmsg': '您输入的密码不合法!'})


        #返回应答
        user = authenticate(username=username,password=password)
        if user is not None:
            #用户名密码正确
            if user.is_active:
                #用户已激活
                #记录用户的登录状态
                login(request,user)

                #获取登录后所要跳转的地址
                #默认跳转到首页
                next_url = request.GET.get('next',reverse('content:index'))

                # 跳转到next_url
                response = redirect(next_url) # HttpResponseRedirect

                # 判断是否需要记住用户名
                remember = request.POST.get('remember')
                if remember == 'on':
                    #记住用户名
                    response.set_cookie('username',username,max_age=7*24*3600)
                else:
                    response.delete_cookie('username')
                #返回response
                return response

            else:
                #用户未激活
                return render(request,'user/login.html',{'errmsg':'您的账号未激活!'})
        else:
            #用户名密码错误
            return render(request,'user/login.html',{'errmsg':'您输入的用户名或密码错误!'})

# /user/logout
class LogoutView(View):
    '''登出'''
    def get(self,request):
        '''登出'''
        #清理用户的session信息
        logout(request)

        #跳转到首页
        return redirect(reverse('con_index:index'))
