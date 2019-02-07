from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.paginator import Paginator
from django.core.cache import cache
from django.db.models import Q


# Create your views here.

#定义视图函数
#/index
#首页页面
class Index(View):
    def get(self,request):

        #request.user
        #如果用户未登录->AnonymousUser类的一个实例
        #如果用户登录->User类的一个实例
        #request.user.is-authenticated()

        #尝试从缓存中获取数据
        context = cache.get('index_page_data')

        if context is None:
            #缓存中没有数据

            from articleOpt.models import article,comment
            #获取文章查询集(前5篇,在模板上进行的数量控制)
            article = article.objects.filter(is_delete=0).order_by('-create_time')
            #获取评论查询集(前6篇,在查询集上进行数量控制)
            comment = comment.objects.filter(is_delete=0).order_by('-create_time')[0:6]

            #组织模板上下文
            context = {
                'article':article,
                'comment':comment,
            }

            #设置缓存
            #key value timeout
            cache.set('index_page_data', context, 3600)

        #除了你给模板文件传递的模板变量之外,django框架会把request.user也传给模板文件
        return render(request, 'content/index.html',context)

#/about
#关于我页面
class About(View):
    def get(self,request):
        return render(request, 'content/about.html')

#/log
#时间轴页面
class log(View):
    def get(self,request,page_num):
        #获取所有文章对象
        from articleOpt.models import article,articleType
        type = articleType.objects.get(type='友情投稿')
        article = article.objects.exclude(type = type).filter(is_delete=0).order_by('-create_time')

        #对数据进行分页
        paginator = Paginator(article,13)

        try:
            #判断传过来的页数参数是否是可以转化为整型
            page = int(page_num)
        except Exception as e:
            page = 1

        #如果当前页大于总页数,使当前页变为第一页
        if page > paginator.num_pages:
            page = 1

        #获取第page页的文章的实例对象
        article_page = paginator.page(page)

        #进行页码的控制,页面上最多显示5个页码
        #1,总页数小于5页,页面上显示所有页码
        #2,如果当前页是前三页,显示1-5页
        #3,如果当前页是后三页,显示后5页
        #4,其他情况,显示当前页的前两页,当前页,当前页的后两页

        #接收一下总页数
        num_pages = paginator.num_pages
        if num_pages < 5:
            pageiter = range(1,num_pages+1)
        elif page <= 3:
            pageiter = range(1,6)
        elif page > (num_pages - 3):
            pageiter = range(num_pages-4,num_pages+1)
        else:
            pageiter = range(page-2,page+3)

        #组织上下文
        context = {
            'article': article_page,
            'num_pages': num_pages,
            'pageiter': pageiter,
        }

        return render(request, 'content/log.html',context)

#/type_article
#查询一类文章的结果显示页面
class type_article(View):
    def get(self,request,artype_id,page_num):
        #查询id是否存在
        #获取类型文章对象
        try:
            from articleOpt.models import articleType,article
            #获取文章类型
            type = articleType.objects.get(id=artype_id)
            #获取满足条件的文章查询集
            article = type.article_set.filter(is_delete=0).order_by('-create_time')
        except:
            return redirect(reverse('content:index'))

        #对数据进行分页
        paginator = Paginator(article,2)

        try:
            #判断传过来的页数参数是否是可以转化为整型
            page = int(page_num)
        except Exception as e:
            page = 1

        #如果当前页大于总页数,使当前页变为第一页
        if page > paginator.num_pages:
            page = 1

        #获取第page页的文章的实例对象
        article_page = paginator.page(page)

        #进行页码的控制,页面上最多显示5个页码
        #1,总页数小于5页,页面上显示所有页码
        #2,如果当前页是前三页,显示1-5页
        #3,如果当前页是后三页,显示后5页
        #4,其他情况,显示当前页的前两页,当前页,当前页的后两页

        #接收一下总页数
        num_pages = paginator.num_pages
        if num_pages < 5:
            pageiter = range(1,num_pages+1)
        elif page <= 3:
            pageiter = range(1,6)
        elif page > (num_pages - 3):
            pageiter = range(num_pages-4,num_pages+1)
        else:
            pageiter = range(page-2,page+3)

        #组织上下文
        context = {
            'type':type,
            'article':article_page,
            'num_pages':num_pages,
            'pageiter':pageiter,
        }

        return render(request, 'content/type_article.html',context)





