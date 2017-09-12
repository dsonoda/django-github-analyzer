from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django_github_analyzer import models
from django_github_analyzer import config
from django_github_analyzer import tasks
from django_github_analyzer import githubs
import datetime
import json

class Command(BaseCommand):
    """
    """
    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for user_info in models.UserInfo.objects.filter(deleted=False).all():
            github = githubs.ModelGithub(access_token=user_info.access_token)
            repository_names = github.get_repository_names()
            for repository_name in repository_names:
                # Repository update date and time in github
                github_updated_at = github.get_repository_info_value('updated_at', repository_name)
                # Repository pull date and time from github
                repository = models.Repository.objects.get(user_info=user_info, name=repository_name, deleted=False)
                # if (repository.pull_at is None) or ((repository.pull_at is not None) and (repository.pull_at < github_updated_at)):
                if True:
                    # Execute parallel processing by Celery for each repository.
                    # issue task queue id
                    queue_id = models.Task.get_queue_id()
                    # Task status regist with 'issue'
                    if models.Task.objects.create(
                        queue_id=queue_id,
                        status=config.TASK_STATUS_ISSUED,
                        mode=config.TASK_MODE_GIT_CLONE,
                        user_info=user_info,
                        repository=repository,
                        start=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    ).id:
                        # Parallel processing start by Celery. The task queue is thrown to RabbitMQ.
                        result = tasks.git_clone.apply_async(
                            (json.dumps({
                                'user_info_login': user_info.login,
                                'repository_name': repository_name,
                            }),
                             queue_id)
                        )
        # for poll_id in options['poll_id']:
        #     self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))
