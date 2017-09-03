import os
import json
from django.shortcuts import render
from django.views import View
from django_github_analyzer import models
from django_github_analyzer import authentications
from django_github_analyzer import githubs
from django.conf import settings


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

        return render(request, 'django_github_analyzer/service_collaborate.html', {
            'input_value': input_value,
            'input_class': input_class,
            'api_url': authentications.Oauth().get_oauth_authorize_uri(),
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

        # get github user information & regist github user information to database
        user_info = githubs.ModelGithub(access_token).get_user_info()
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
