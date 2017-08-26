from django.db import models
from github_analyzer import config
import time


class UserInfo(models.Model):
    """
    Github user information
    """
    # Github login id
    login = models.TextField(null=True)
    # URL
    url = models.TextField(null=True)
    # Github application Client ID
    client_id = models.TextField(null=True)
    # Github application Client Secret
    client_secret = models.TextField(null=True)
    # Github access token
    access_token = models.TextField(null=True)
    # Github information（format:JSON）
    params = models.TextField(null=True)
    # registed datetime
    created = models.DateTimeField(auto_now_add=True)
    """
    delete flg
        True: record used in the system
        False: record not used in the system
    """
    deleted = models.BooleanField(u'delete flg', default=False)

    def __str__(self):
        return self.login


class SourceCode(models.Model):
    pass