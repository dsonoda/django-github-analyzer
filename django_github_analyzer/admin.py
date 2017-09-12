from django.contrib import admin
from django_github_analyzer import models

@admin.register(models.UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('login', 'name', 'html_url', 'deleted')

@admin.register(models.Repository)
class RepositoryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'language', 'git_url', 'private', 'fork', 'clone_at', 'pull_at', 'analysis_at', 'deleted')

@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('queue_id', 'status', 'mode', 'user_info', 'repository', 'start', 'end', 'deleted')
