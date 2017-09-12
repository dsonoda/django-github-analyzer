from django.core.management.base import BaseCommand, CommandError
from django_github_analyzer import models
from django_github_analyzer import config
from django_github_analyzer import tasks
from django_github_analyzer import githubs
from django.conf import settings
import datetime
import json

class Command(BaseCommand):
    """Git clone
    """
    def handle(self, *args, **options):
        for user_info in models.UserInfo.objects.filter(deleted=False).all():
            github = githubs.ModelGithub(access_token=user_info.access_token)
            # Only those repositories that have not yet been git cloned are processed
            repositories = models.Repository.objects.filter(user_info=user_info, clone_at=None, deleted=False)
            for repository in repositories:
                # repository filter by private or fork
                if github.filter_repository_info(private=repository.private, fork=repository.fork):
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
                                'git_url': repository.git_url,
                                'user_info_login': user_info.login,
                                'repository_name': repository.name,
                            }),
                             queue_id)
                        )
