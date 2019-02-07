from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from utils.mixin import LoginRequireMixin
from django.views.generic import View
from django.http import JsonResponse
#Ueditor用得到
from django.forms import forms
from DjangoUeditor.forms import UEditorField
# Create your views here.

#/articleRead
#读单个文章所在页面的加载
class ArticleRead(View):

    def get(self,request,art_id):

        #map函数的第一个参数(函数,用来处理并返回一个元组)
        def buildset(x):
            #以回复的时间倒序排序,排除带有删除标记的回复
            return(x.reply_set.all().filter(is_delete=0).order_by('-create_time'),x)

        try:
            #通过文章id后去文章对象
            from articleOpt.models import article, comment
            article = article.objects.get(id=art_id)
            #如果文章被删除标记,产生不存在异常
            if article.is_delete == 1:
                raise article.DoesNotExist
        except article.DoesNotExist:
            #文章不存在,返回首页
            return redirect(reverse('content:index'))

        #获取文章所对应的所有评论子集以创建时间的倒序排序,排除带有删除标记的评论
        comment =article.comment_set.all().filter(is_delete=0).order_by('-create_time')

        #评论个数
        comcount = comment.count()

        #组织上下文
        context = {
            'article':article,
            'comment':comment,
            'comcount':comcount,
            'map':map(buildset,comment)
        }
        return render(request, 'articleOpt/articleRead.html',context)

#富文本类,提供前端富文本显示
class DjangoueditorForm(forms.Form):
    content = UEditorField('', width=800, height=300, toolbars="full",upload_settings = {"imageMaxSize": 1204000},settings = {})

# /articleWrite
#文章的写入页面
class ArticleWriteView(LoginRequireMixin,View):
    def get(self,request):
        forms = DjangoueditorForm()
        return render(request, 'articleOpt/articleWrite.html', {'forms':forms})
    def post(self,request):
        user = request.user
        if not user.is_authenticated():
            #用户未登录
            return JsonResponse({'errmsg':'您未登录!'})
        #接收数据
        try:
            #文章标题
            title = request.POST.get('title')
            #文章描述
            describe = request.POST.get('describe')
            #数据合法性验证
            if (1 > len(title)) or (len(title) > 20) or (1 > len(describe)) or (len(describe) >20):
                return JsonResponse({'errmsg':'您未输入标题和描述或它们长度超过20!'})
            #文章类型
            artype = request.POST.get('artype')
            if artype not in ['友情投稿','网站建设','Python','Java','前端','life']:
                artype = '友情投稿'
            #文章内容
            detail = request.POST.get('detail')
            #文章作者对象,和文章类型对象
            from user.models import User
            from articleOpt.models import articleType
            userid = request.user.id
            user = User.objects.get(id=userid)
            type = articleType.objects.get(type=artype)
        except:
            return JsonResponse({'errmsg':'您输入的数据不完整!'})
        #写入数据库
        try:
            from articleOpt.models import article
            article = article()
            article.title = title
            article.descriptive = describe
            article.type = type
            article.detail = detail
            article.user = user
            #默认文章都打删除标记
            article.is_delete = 1
            article.save()
        except:
            return JsonResponse({'errmsg':'写入数据库失败!'})
        return  JsonResponse({'res':2,'errmsg':'您的文章上传成功,待审核后发表!'})

#/commentWrite
#评论的写入
#继承LoginRequireMixin类,避免用户直接输入路由地址访问
class commentWrite(LoginRequireMixin,View):
    def post(self,request):
        #判断发起post请求的用户是否登录
        user = request.user
        if not user.is_authenticated():
            #用户未登录
            return JsonResponse({'errmsg':'您未登录!'})
        #接收数据
        try:
            #被评论的文章id
            article_id = request.POST.get('article_id')
            #评论内容
            comment_detail = request.POST.get('comment_detail')
            #评论者
            username = request.user.username
            from user.models import User
            user = User.objects.get(username=username)
            from articleOpt.models import article
            article = article.objects.get(id=article_id)
        except:
            return JsonResponse({'errmsg':'获取数据失败!'})
        #写入数据库
        try:
            from articleOpt.models import comment
            comment = comment()
            comment.detail = comment_detail
            #绑定的外键均为对象,所以先获取对象
            comment.user = user
            comment.article = article
            comment.save()
        except:
            return JsonResponse({'写入数据库失败!'})
        return JsonResponse({'res':2,'errmsg':'您评论成功了哦!'})

#/replyWrite
#回复的写入
# 继承LoginRequireMixin类,避免用户直接输入路由地址访问
class replyWrite(LoginRequireMixin,View):
    def post(self,request):
        # 判断发起post请求的用户是否登录
        user = request.user
        if not user.is_authenticated():
            #用户未登录
            return JsonResponse({'errmsg':'您未登录!'})
        # 接收数据
        try:
            #被回复者的用户名
            reply_obj = request.POST.get('reply_obj')
            #回复内容
            reply_detail = ' 回复 '+reply_obj+": "+request.POST.get('reply_detail')
            #所属那条评论的id
            reply_comm = int(request.POST.get('reply_comm'))
            username = request.user.username
            #获取评论者的对象
            from user.models import User
            user = User.objects.get(username=username)
            #获取回复所属的那条评论的对象
            from articleOpt.models import comment
            comment = comment.objects.get(id=reply_comm)
        except:
            return  JsonResponse({'errmsg':'获取数据失败!'})
        #写入数据库
        try:
            from articleOpt.models import reply
            reply = reply()
            reply.detail = reply_detail
            # 绑定的外键均为对象,所以先获取对象
            reply.user = user
            reply.comment = comment
            reply.save()
        except:
            return JsonResponse({'errmsg':'写入数据库失败!'})
        return JsonResponse({'res':2,'errmsg':'您回复成功了哦!'})

