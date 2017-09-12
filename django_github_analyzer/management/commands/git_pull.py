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
