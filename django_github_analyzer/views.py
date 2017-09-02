import os
import urllib.parse
import requests
import json
from django.shortcuts import render
from django.views import View
from django_github_analyzer import models
from django_github_analyzer import credentials
from django_github_analyzer import config
from django_github_analyzer import authentications
from django_github_analyzer import githubs


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








        oauth = authentications.Oauth(
            client_id=credentials.client_id,
            client_secret=credentials.client_secret,
        )
        # get oauth uri
        api_url = oauth.get_oauth_authorize_uri()
        return render(request, 'django_github_analyzer/service_collaborate.html', {
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
        oauth = authentications.Oauth(
            client_id=credentials.client_id,
            client_secret=credentials.client_secret,
        )
        # get access token
        access_token = oauth.get_access_token(request.GET.get('code'))
        # get github user information
        user_info = githubs.ModelGithub(access_token).get_user_info()
        # regist github user information to database
        if models.UserInfo.objects.filter(login=user_info['login']).count() == 0:
            models.UserInfo.objects.create(
                login=user_info['login'],
                url=user_info['html_url'],
                client_id=oauth.get_client_id(),
                client_secret=oauth.get_client_secret(),
                access_token=access_token,
                params=json.dumps(user_info)
            )

        return render(request, 'django_github_analyzer/oauth_callback.html', {})
