from django.shortcuts import render
from django.views import View
from django_github_analyzer import config
from django_github_analyzer import models
from django_github_analyzer import authentications
from django_github_analyzer import githubs
from django_github_analyzer import tasks
from django.conf import settings
import datetime
import json


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
        # github = githubs.ModelGithub(access_token="8faf2da99c9b05f15a13b8e37e01e928013660cf")
        # raise Exception(github.get_user_info("8faf2da99c9b05f15a13b8e37e01e928013660cf"))
        # raise Exception(github.get_user_info())
        # raise Exception(github.get_user_info())
        # res = github.git_clone('git://github.com/dsonoda/template-tweeter.git', 'dsonoda', 'template-tweeter')
        # raise Exception(res)




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
        # github object (about this user)
        github = githubs.ModelGithub(access_token=access_token)
        # get github user information
        github_user_info = github.get_user_info()
        # regist github user information to database
        models.UserInfo.objects.regist_data(github_user_info['login'], access_token, github_user_info)
        user_info = models.UserInfo.objects.get(login=github_user_info['login'], deleted=False)
        # get github repository information & regist to database
        repository_names = github.get_repository_names()
        for repository_name in repository_names:
            """Execute parallel processing by Celery for each repository.
            """
            # issue task queue id
            queue_id = models.Task.get_queue_id()
            # Task status regist with 'issue'
            if models.Task.objects.create(
                queue_id=queue_id,
                status=config.TASK_STATUS_ISSUED,
                mode=config.TASK_MODE_REPOSITORY_INFO_REGIST,
                user_info=user_info,
                start=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ).id:
                # Parallel processing start by Celery. The task queue is thrown to RabbitMQ.
                result = tasks.regist_repository.apply_async(
                    (json.dumps({
                        'user_info_login': user_info.login,
                        'repository_name': repository_name,
                    }),
                    queue_id)
                )
        return render(request, 'django_github_analyzer/oauth_callback.html', {})
