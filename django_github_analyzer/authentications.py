import os
import urllib.parse
import requests
from django_github_analyzer import config


class Oauth():
    """
    OAuth authentication module.
    """

    "Github client id"
    __client_id = None
    "Github client secret"
    __client_secret = None
    "my project url (ex. https://yoursiteurl.com"
    __site_url = None


    def __init__(self, **args):
        """
        Constructor
        :param client_id (*Required): github application client id
        :param client_secret (*Required): github application client secret
        :param site_url: my project url (ex. https://yoursiteurl.com
        """
        # set github client id
        if 'client_id' in args:
            self.__set_client_id(args['client_id'])
        elif os.environ.get("GITHUB_OAUTH_CLIENT_ID") != None:
            self.__set_client_id(os.environ.get("GITHUB_OAUTH_CLIENT_ID"))
        # set github client secret
        if 'client_secret' in args:
            self.__set_client_secret(args['client_secret'])
        elif os.environ.get("GITHUB_OAUTH_CLIENT_SECRET") != None:
            self.__set_client_secret(os.environ.get("GITHUB_OAUTH_CLIENT_SECRET"))
        # set site url
        if 'site_url' in args:
            self.__set_site_url(args['site_url'])

        if self.get_client_id() == None or self.get_client_secret() == None:
            raise Exception("error! Argument is missing.")


    def __set_client_id(self, client_id):
        """
        setter github client id
        :param client_id:
        :return:
        """
        self.__client_id = client_id


    def get_client_id(self):
        """
        getter github client id
        :return:
        """
        return self.__client_id


    def __set_client_secret(self, client_secret):
        """
        setter github client secret
        :param client_secret:
        :return:
        """
        self.__client_secret = client_secret


    def get_client_secret(self):
        """
        getter github client secret
        :return:
        """
        return self.__client_secret


    def __set_site_url(self, site_url):
        """
        setter mysite url
        :param site_url:
        :return:
        """
        self.__site_url = site_url


    def get_site_url(self):
        """
        getter mysite url
        :return:
        """
        return self.__site_url


    def get_oauth_authorize_uri(self):
        """
        Get Github OAuth api url
        :return:
        """
        params = {'client_id': self.__client_id}
        if self.get_site_url() != None:
            params['redirect_uri'] = self.get_site_url().strip('/') + '/' + config.django_callback_url.strip('/')
        if len(config.scope) != 0:
            params['scope'] = config.scope
        return config.oauth_authorize_uri.strip('/') + '/?' + urllib.parse.urlencode(params, quote_via=urllib.parse.quote)


    def get_access_token(self, code):
        """
        Get Github Access Token
        :param code:
        :return:
        """
        if len(code) == 0:
            return ''
        params = {
            'client_id': self.__client_id,
            'client_secret': self.__client_secret,
            'code': code,
        }
        api_url = config.oauth_access_token_uri.strip('/') + '/?' + urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
        r = requests.post(api_url)
        return urllib.parse.parse_qs(r.text)['access_token'][0]