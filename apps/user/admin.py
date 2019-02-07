from django.contrib import admin
from user.models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['id','create_time','is_delete']

admin.site.register(User,UserAdmin)