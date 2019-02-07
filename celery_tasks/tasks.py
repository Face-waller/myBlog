#使用celery

from celery import Celery
from django.template import loader,RequestContext

# 创建一个Celery实例对象
from django.conf import settings
from django.core.mail import send_mail

#在任务处理者一端加入以下几句
#django环境的初始化
import os
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myBlog.settings")
# django.setup()

app = Celery('celery_tasks.tasks',broker='redis://192.168.31.149:6379/8')

#定义任务函数
@app.task
def send_register_active_email(to_email,username,token):
    '''发送激活邮件'''
    #组织邮件信息
    subject = '番茄博客欢迎信息'
    message = '%s,欢迎您使用番茄博客!请转到下面链接激活您的账号\r\nhttp://127.0.0.1/active/%s' % (username, token)
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    # html_message = '<h1>%s,欢迎您使用番茄博客!</h1>请点击下面链接激活您的账号</br><a href="http://127.0.0.1/active/%s">http://127.0.0.1/active/%s</a>'%(username,token,token)
    send_mail(subject, message, sender, receiver)

@app.task
def generate_static_index_html():
    '''产生未登录用户的首页静态页面'''

    #在任务处理者中导入模型类需要在上面初始化后导入,否则找不到
    from articleOpt.models import article, comment
    # 获取文章查询集(前5篇,通过在模板上进行的数量控制)
    article = article.objects.filter(is_delete=0).order_by('-create_time')
    # 获取评论查询集(前6篇,通过在查询集上进行数量控制)
    comment = comment.objects.filter(is_delete=0).order_by('-create_time')[0:6]

    # 组织模板上下文
    context = {
        'article': article,
        'comment': comment,
    }

    #使用模板
    #1.加载模板文件,返回模板对象
    temp = loader.get_template('content/static_index.html')
    #2.模板渲染
    static_index_html = temp.render(context)

    #生成首页对应静态文件
    save_path = os.path.join(settings.BASE_DIR, 'static/index.html')
    with open(save_path, 'w') as f:
        f.write(static_index_html)