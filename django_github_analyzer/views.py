from django.shortcuts import render
from django.views import View
from django_github_analyzer import models
from django_github_analyzer import authentications
from django_github_analyzer import githubs
from django_github_analyzer import config
from django.conf import settings


class ServiceCollaborateView(View):
    """Pages of form linking services through OAuth authentication.
    """

    def get(self, request):
        """Service Collaborate form.
        :param request :
        :return: render
        """


        # 8faf2da99c9b05f15a13b8e37e01e928013660cf
        # github = githubs.ModelGithub()
        github = githubs.ModelGithub(access_token="8faf2da99c9b05f15a13b8e37e01e928013660cf")
        # github.set_access_token("8faf2da99c9b05f15a13b8e37e01e928013660cf")
        # raise Exception(github.get_user_info("8faf2da99c9b05f15a13b8e37e01e928013660cf"))
        # raise Exception(github.get_user_info())
        res = github.git_clone('git://github.com/dsonoda/template-tweeter.git', 'dsonoda', 'template-tweeter')
        raise Exception(res)




        # get github oauth url
        api_url = authentications.Oauth().get_oauth_authorize_uri()
        # set input button class name
        input_class = ''
        try:
            input_class = settings.GITHUB_OAUTH_BUTTON_CLASS
        except:
            input_class = config.GITHUB_OAUTH_BUTTON_CLASS
        # set input button value
        input_value = ''
        try:
            input_value = settings.GITHUB_OAUTH_BUTTON_VALUE
        except:
            input_value = config.GITHUB_OAUTH_BUTTON_VALUE
        # set input button id
        input_id = ''
        try:
            input_id = settings.GITHUB_OAUTH_BUTTON_ID
        except:
            input_id = config.GITHUB_OAUTH_BUTTON_ID
        return render(request, 'django_github_analyzer/service_collaborate.html', {
            'api_url': api_url,
            'input_class': input_class,
            'input_value': input_value,
            'input_id': input_id,
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
        github = githubs.ModelGithub()

        # get github user information & regist to database
        user_info = github.get_user_info(access_token)
        models.UserInfo.objects.regist_data(user_info['login'], access_token, user_info)

        # get github repository information & regist to database
        user_info = models.UserInfo.objects.get(login=user_info['login'], deleted=False)
        repository_names = github.get_repository_names(access_token)
        for repository_name in repository_names:
            models.Repository.objects.regist_data(
                user_info,
                repository_name,
                github.get_repository_info(repository_name, access_token)
            )

        return render(request, 'django_github_analyzer/oauth_callback.html', {})
