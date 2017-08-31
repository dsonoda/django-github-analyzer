import os
import urllib.parse
import requests
from django_github_analyzer import config


class Oauth():
    """
    OAuth authentication module.
    """

    def __init__(self, site_url):
        """
        Constructor
        :param site_url: your project url (ex. https://yoursiteurl.com
        """
        if len(site_url) == 0:
            self.site_url = config.site_url

    def get_oauth_authorize_uri(self):
        """
        Get Github OAuth api url
        :return:
        """
        params = {
            'client_id': os.environ['GITHUB_OAUTH_CLIENT_ID'],
            'redirect_uri': self.site_url.strip('/') + '/' + config.django_callback_url.strip('/'),
            'scope': config.scope,
        }
        return config.oauth_authorize_uri.strip('/') + '/?' + urllib.parse.urlencode(params, quote_via=urllib.parse.quote)

    def get_access_token(self, code):
        """
        Get Github Access Token
        :param code:
        :return:
        """
        params = {
            'client_id': os.environ['GITHUB_OAUTH_CLIENT_ID'],
            'client_secret': os.environ['GITHUB_OAUTH_CLIENT_SECRET'],
            'code': code,
        }
        api_url = config.oauth_access_token_uri.strip('/') + '/?' + urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
        r = requests.post(api_url)
        return urllib.parse.parse_qs(r.text)['access_token'][0]