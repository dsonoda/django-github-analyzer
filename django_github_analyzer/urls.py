from django.conf.urls import url
from django_github_analyzer.views import ServiceCollaborateView, OauthCallbackView


urlpatterns = [
    url(r'^service_collaborate/$', ServiceCollaborateView.as_view(), name='service_collaborate'),
    url(r'^oauth_callback/$', OauthCallbackView.as_view(), name='oauth_callback'),
]
