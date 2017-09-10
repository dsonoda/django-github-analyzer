"""
In this module, only processing related to OAuth authentication using the Github API is executed.
:see: https://developer.github.com/apps/building-integrations/setting-up-and-registering-oauth-apps/registering-oauth-apps/
"""

import os
import urllib.parse
import requests
from django_github_analyzer import config
from django.conf import settings


class Oauth():
    """OAuth authentication module.
    """

    """Github client id
    :type: string or None
    """
    __client_id = None

    """Github client secret
    :type: string or None
    """
    __client_secret = None

    """Github callback uri
    :type: string or None
    """
    __callback_uri = None

    def __init__(self, **args):
        """Initial settings.
        :param client_id (string): Github application client id.
        :param client_secret (string): Github application client secret.
        :param callback_uri (string): Github oauth callback uri.
        """
        # set github client id
        if 'client_id' in args:
            self.__set_client_id(args['client_id'])
        elif os.environ.get('GITHUB_OAUTH_CLIENT_ID') != None:
            self.__set_client_id(os.environ.get('GITHUB_OAUTH_CLIENT_ID'))

        # set github client secret
        if 'client_secret' in args:
            self.__set_client_secret(args['client_secret'])
        elif os.environ.get('GITHUB_OAUTH_CLIENT_SECRET') != None:
            self.__set_client_secret(os.environ.get('GITHUB_OAUTH_CLIENT_SECRET'))

        if self.get_client_id() == None or self.get_client_secret() == None:
            raise Exception("error! Argument is missing.")

        # set callback url
        if 'callback_uri' in args:
            self.__set_callback_uri(args['callback_uri'])
        else:
            try:
                self.__set_callback_uri(settings.GITHUB_OAUTH_CALLBACK_URI)
            except:
                raise Exception("error! Argument is missing.")

    def __set_client_id(self, client_id):
        """Setter github client id.
        :param client_id (string): Github application client id.
        """
        self.__client_id = client_id

    def get_client_id(self):
        """Getter github client id.
        :return: string
        """
        return self.__client_id

    def __set_client_secret(self, client_secret):
        """Setter github client secret.
        :param client_secret (string): Github application client secret.
        """
        self.__client_secret = client_secret

    def get_client_secret(self):
        """Getter github client secret.
        :return: string
        """
        return self.__client_secret

    def __set_callback_uri(self, callback_uri):
        """Setter oauth callback uri.
        :param callback_uri (string): Github oauth callback uri.
        """
        self.__callback_uri = callback_uri

    def get_callback_uri(self):
        """Getter oauth callback uri.
        :return: string
        """
        return self.__callback_uri

    def get_oauth_authorize_uri(self):
        """Get github OAuth api url.
        :return: string
        """
        params = {
            'client_id': self.get_client_id(),
            'redirect_uri': self.get_callback_uri(),
        }
        try:
            if len(settings.GITHUB_OAUTH_URI_PARAMS_SCOPE):
                params['scope'] = settings.GITHUB_OAUTH_URI_PARAMS_SCOPE
        except:
            pass
        return config.OAUTH_AUTHORIZE_URI.strip('/') + '/?' + urllib.parse.urlencode(params, quote_via=urllib.parse.quote)

    def get_access_token(self, code):
        """Get github access token.
        :param code:
        :return: string
        """
        if len(code) == 0:
            raise Exception("error! Argument is missing.")
        params = {
            'client_id': self.__client_id,
            'client_secret': self.__client_secret,
            'code': code,
        }
        api_url = config.OAUTH_ACCESS_TOKEN_URI.strip('/') + '/?' + urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
        r = requests.post(api_url)
        return urllib.parse.parse_qs(r.text)['access_token'][0]