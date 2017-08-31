from django.contrib import admin
from django_github_analyzer import models

@admin.register(models.UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    pass