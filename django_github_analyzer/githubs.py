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

    "Github access token"
    __access_token = None


    def __init__(self, access_token):
        """
        Constructor
        :param access_token (*Required): github application access token
        """
        # set github access token
        if len(access_token) != 0:
            self.__set_access_token(access_token)

        if self.get_access_token() == None:
            raise Exception("error! Argument is missing.")


    def __set_access_token(self, access_token):
        """
        setter github access token
        :param access_token:
        :return:
        """
        self.__access_token = access_token


    def get_access_token(self):
        """
        getter github access token
        :return:
        """
        return self.__access_token


    def get_user_info(self):
        """
        get user information by access token.
        :return: 
        """
        params = {'access_token': self.get_access_token()}
        api_url = config.get_user_information_uri.strip('/') + '?' + urllib.parse.urlencode(params)
        r = requests.get(api_url)
        return r.json()
