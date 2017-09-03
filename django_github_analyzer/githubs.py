import os
import urllib.parse
import requests
from github import Github
from django_github_analyzer import config


class ModelGithub():
    """Github information module.
    """

    """Github access token
    :type: string or None
    """
    __access_token = None

    def __init__(self, access_token):
        """Initial settings.
        :param access_token (string): github application access token.
        """
        # set github access token
        if len(access_token) != 0:
            self.__set_access_token(access_token)
        else:
            raise Exception("error! Argument is missing.")

    def __set_access_token(self, access_token):
        """Setter github access token
        :param access_token (string): github application access token.
        """
        self.__access_token = access_token

    def get_access_token(self):
        """Getter github access token
        :return: string
        """
        return self.__access_token

    def get_user_info(self):
        """Get user information by access token.
        :return: string
        """
        params = {'access_token': self.get_access_token()}
        api_url = config.get_user_information_uri.strip('/') + '?' + urllib.parse.urlencode(params)
        r = requests.get(api_url)
        return r.json()
