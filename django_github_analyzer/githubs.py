import os
import urllib.parse
import requests
import json
from django_github_analyzer import models
from django_github_analyzer import config

class ModelGithub():
    """
    Github information module.
    """

    def __init__(self, access_token):
        """
        Constructor
        :param access_token: github access token
        """
        self.access_token = access_token

    def get_user_info(self):
        """
        Get user information by Github
        :return:
        """
        params = {'access_token': self.access_token}
        api_url = config.get_user_information_uri.strip('/') + '?' + urllib.parse.urlencode(params)
        r = requests.get(api_url)
        return r.json()