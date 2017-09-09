import os
import json
from django.shortcuts import render
from django.views import View
from django_github_analyzer import models
from django_github_analyzer import authentications
from django_github_analyzer import githubs
from django.conf import settings

from github import Github

class ServiceCollaborateView(View):
    """Pages of form linking services through OAuth authentication.
    """

    def get(self, request):
        """Service Collaborate form.
        :param request :
        :return: render
        """
        # set input button value
        input_value = ''
        try:
            input_value = settings.GITHUB_OAUTH_BUTTON_VALUE
        except:
            pass

        # set input button class name
        input_class = ''
        try:
            input_class = settings.GITHUB_OAUTH_BUTTON_CLASS
        except:
            pass

        # get github oauth url
        api_url = authentications.Oauth().get_oauth_authorize_uri()

        return render(request, 'django_github_analyzer/service_collaborate.html', {
            'input_value': input_value,
            'input_class': input_class,
            'api_url': api_url,
        })


class OauthCallbackView(View):
    """OAuth callback page from Github.
    """

    def get(self, request):
        """Get access code and user information, and database resitration.
        :param request :
        :return: render
        """
        # get access token
        oauth = authentications.Oauth()
        access_token = oauth.get_access_token(request.GET.get('code'))

        # github object
        github = githubs.ModelGithub(access_token)

        # get github user information & regist to database
        user_info = github.get_user_info()
        models.UserInfo.objects.registData(user_info['login'], access_token, user_info)

        # get github repository information & regist to database
        user_info = models.UserInfo.objects.get(login=user_info['login'], deleted=False)
        repo_names = github.get_repo_names()
        for repo_name in repo_names:
            models.Repository.objects.registData(user_info, repo_name, github.get_repo_info(repo_name))

        return render(request, 'django_github_analyzer/oauth_callback.html', {})
