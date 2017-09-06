import os
import urllib.parse
import requests
from github import Github
from django_github_analyzer import config


class ModelGithub():
    """Github information module.
    """

    # PyGithub object
    __github = None

    """Github access token
    :type: string or None
    """
    __access_token = None

    def __init__(self, access_token):
        """Initial settings.
        :param access_token (string): github application access token.
        """
        # set PyGithub object
        self.__github = Github(access_token)
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
        u = self.__github.get_user()
        # print(u.id)
        # print(u.html_url)
        # print(u.name)
        # print(u.email)
        # print(u.bio)
        # print(u.location)
        # print(u.company)


        params = {'access_token': self.get_access_token()}
        api_url = config.get_user_information_uri.strip('/') + '?' + urllib.parse.urlencode(params)
        r = requests.get(api_url)
        return r.json()
