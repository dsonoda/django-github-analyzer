from mysite.celery import app as celery_app
from celery.utils.log import get_task_logger
from django_github_analyzer import githubs
from django_github_analyzer import models
from django_github_analyzer import config
from django.conf import settings
import json


logger = get_task_logger(__name__)

@celery_app.task(bind=True)
def git_clone(self, request, queue_id):
    """Execute parallel processing by Celery for each user.
    :param request: parameter
    :param queue_id: task queue id
    :return:
    """
    params = json.loads(request)
    user_info = params['user_info']
    github = githubs.ModelGithub(access_token=user_info.access_token)
    repository_names = github.get_repository_names()
    for repository_name in repository_names:
        # regist repository data
        repository = github.get_repository_info(repository_name)
        models.Repository.objects.regist_data(
            user_info,
            repository_name,
            repository
        )
        res = github.git_clone(repository['git_url'], user_info.login, repository_name)

    # raise Exception(github.get_repository_info_value('updated_at', 'template-tweeter'))
    # raise Exception(models.Repository.objects.get_param_value('pull_at', 'dsonoda', 'template-tweeter'))

