from django.contrib import admin
from django_github_analyzer import models

@admin.register(models.UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Repository)
class RepositoryAdmin(admin.ModelAdmin):
    pass