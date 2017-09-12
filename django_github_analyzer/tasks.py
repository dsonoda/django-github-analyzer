from mysite.celery import app as celery_app
from celery.utils.log import get_task_logger
from django_github_analyzer import githubs
from django_github_analyzer import models
from django_github_analyzer import config
from django.conf import settings
import datetime
import json


logger = get_task_logger(__name__)


@celery_app.task(bind=True)
def regist_repository(self, request, queue_id):
    """Resist github information to database
    :param request (string: json.dump()): parameter
    :param queue_id (string):
    :return (string): queue_id
    """
    # Task status update to 'start'
    t = models.Task.objects.get(
        queue_id=queue_id,
        mode=config.TASK_MODE_REPOSITORY_INFO_REGIST,
        end=None,
        deleted=False)
    t.status=config.TASK_STATUS_START
    t.save()

    # load request
    params = json.loads(request)
    # get UserInfo
    user_info = models.UserInfo.objects.get(login=params['user_info_login'], deleted=False)
    # get repository info from Github
    github = githubs.ModelGithub(access_token=user_info.access_token)
    repository = github.get_repository_info(params['repository_name'])
    # regist repository data
    models.Repository.objects.regist_data(
        user_info,
        repository['name'],
        repository
    )

    # Task status update to 'end'
    t = models.Task.objects.get(
        queue_id=queue_id,
        mode=config.TASK_MODE_REPOSITORY_INFO_REGIST,
        end=None,
        deleted=False)
    t.status=config.TASK_STATUS_END
    t.end=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    t.save()
    return queue_id

@celery_app.task(bind=True)
def git_clone(self, request, queue_id):
    """Execute parallel processing by Celery for each user.
    :param request (string: json.dump()): parameter
    :param queue_id (string):
    :return (string): queue_id
    """
    # Task status update to 'start'
    t = models.Task.objects.get(
        queue_id=queue_id,
        mode=config.TASK_MODE_GIT_CLONE,
        end=None,
        deleted=False)
    t.status=config.TASK_STATUS_START
    t.save()

    # load request
    params = json.loads(request)
    user_info = models.UserInfo.objects.get(login=params['user_info_login'], deleted=False)
    # git clone
    github = githubs.ModelGithub(access_token=user_info.access_token)
    res = github.git_clone(params['git_url'], params['user_info_login'], params['repository_name'])

    # update Repository data
    updatetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    repositories = models.Repository.objects.get(user_info=user_info, name=params['repository_name'], pull_at=None, deleted=False)
    repositories.updated_at = updatetime
    repositories.clone_at = updatetime
    repositories.pull_at = updatetime
    repositories.save()

    # Task status update to 'end'
    t = models.Task.objects.get(
        queue_id=queue_id,
        mode=config.TASK_MODE_GIT_CLONE,
        end=None,
        deleted=False)
    t.status=config.TASK_STATUS_END
    t.end=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    t.save()
    return queue_id
