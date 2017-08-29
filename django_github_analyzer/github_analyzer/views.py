import os
import urllib.parse
import requests
import json
from django.shortcuts import render
from django.views import View
from github_analyzer import models
from github_analyzer import config


class ServiceCollaborateView(View):
    """
    Pages of form linking services through OAuth authentication
    """
    def get(self, request):
        """
        Service Collaborate form.
        :param request:
        :return:
        """
        redirect_uri = os.environ['DJANGO_GITHUB_OAUTH_PROJECT_URL'].strip('/') + '/' + config.django_callback_url.strip('/')
        params = {
            'client_id': os.environ['GITHUB_OAUTH_CLIENT_ID'],
            'redirect_uri': redirect_uri,
            'scope': config.scope,
        }
        api_url = config.oauth_authorize_uri.strip('/') + '/?' + urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
        return render(request, 'github_analyzer/service_collaborate.html', {
            'input_value': config.button_value,
            'input_class': config.button_class,
            'api_url': api_url,
        })


class OauthCallbackView(View):
    """
    OAuth callback page from Github.
    """
    def get(self, request):
        """
        Get access code and user information, and database resitration.
        :param request:
        :return:
        """
        # get access token
        params = {
            'client_id': os.environ['GITHUB_OAUTH_CLIENT_ID'],
            'client_secret': os.environ['GITHUB_OAUTH_CLIENT_SECRET'],
            'code': request.GET.get('code'),
        }
        api_url = config.oauth_access_token_uri.strip('/') + '/?' + urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
        r = requests.post(api_url)
        access_token = urllib.parse.parse_qs(r.text)['access_token'][0]
        # get github user information
        params = {
            'access_token': access_token,
        }
        api_url = config.get_user_information_uri.strip('/') + '?' + urllib.parse.urlencode(params)
        r = requests.get(api_url)
        user_info = r.json()
        # regist user infomation by Github
        if models.UserInfo.objects.filter(login=user_info['login']).count() == 0:
            models.UserInfo.objects.create(
                login=user_info['login'],
                url=user_info['html_url'],
                client_id=os.environ['GITHUB_OAUTH_CLIENT_ID'],
                client_secret=os.environ['GITHUB_OAUTH_CLIENT_SECRET'],
                access_token=access_token,
                params=json.dumps(user_info)
            )

        return render(request, 'github_analyzer/oauth_callback.html', {})
