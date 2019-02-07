from django.contrib import admin
from articleOpt.models import *
from django.core.cache import cache

# Register your models here.

#使需要在数据新增,更新,删除时,重新生成静态首页页面的管理类继承下面这个类
#此类重写了两个方法,但保留了原有方法的功能
class BaseModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        '''新增或更新表中的数据时调用'''
        super().save_model(request, obj, form, change)

        #发出任务,让celery worker重新生成首页静态页
        from celery_tasks.tasks import generate_static_index_html
        generate_static_index_html.delay()

        # 清除首页的缓存存储
        cache.delete('index_page_data')

    #由于此项目不涉及删除数据,删除文章等通过更新删除标记的属性的方式,但此处仍然抛砖引玉,为了完整性,重写下列方法
    def delete_model(self, request, obj):
        '''删除表中的数据时调用'''
        super().delete_model(request,obj)

        #发出任务,让celery worker重新生成首页静态页
        from celery_tasks.tasks import generate_static_index_html
        generate_static_index_html.delay()

        # 清除首页的缓存存储
        cache.delete('index_page_data')


class articleTypeAdmin(admin.ModelAdmin):
    list_display = ['id','type']

class articleAdmin(BaseModelAdmin):
    list_display = ['id','title','is_secrete','is_delete','user','type']

class replyAdmin(admin.ModelAdmin):
    list_display = ['user','comment','is_delete','detail']

class commentAdmin(BaseModelAdmin):
    list_display = ['user','article','is_delete','detail']

admin.site.register(articleType,articleTypeAdmin)
admin.site.register(article,articleAdmin)
admin.site.register(reply,replyAdmin)
admin.site.register(comment,commentAdmin)



