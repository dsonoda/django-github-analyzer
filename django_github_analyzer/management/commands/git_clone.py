from django.core.management.base import BaseCommand, CommandError
from django_github_analyzer import models
from django_github_analyzer import tasks
from django_github_analyzer import config
from django.conf import settings

import datetime
import json

class Command(BaseCommand):
    """
    """
    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for user_info in models.UserInfo.objects.filter(deleted=False).all():
            # Execute parallel processing by Celery for each user.
            queue_id = models.Task.get_queue_id()
            # regist Task
            if models.Task.objects.create(
                queue_id=queue_id,
                status=config.TASK_STATUS_ISSUED,
                mode=config.TASK_MODE_GIT_CLONE,
                user_info=user_info,
                start=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ).id:
                # Parallel processing start by Celery. The task queue is thrown to RabbitMQ.
                result = tasks.git_clone.apply_async(
                    (json.dumps({
                        'user_info': user_info,
                    }),
                    queue_id)
                )

        # for poll_id in options['poll_id']:
        #     self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))
