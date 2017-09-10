from django import template
from django.utils.safestring import mark_safe
from django_github_analyzer import config
from django.conf import settings


register = template.Library()

@register.assignment_tag
def oauth_button(api_url, input_class, input_value, input_id):
    """Output Github service collaboration button
    :param api_url: Github OAuth API URL (http://github.com/login/oauth/authorize) + query parameters
    :param input_class: class name for button decoration
    :param input_value: button word
    :param input_id: button id
    :return: html tag
    """
    # set input button class name
    if input_class == '':
        try:
            input_class = settings.GITHUB_OAUTH_BUTTON_CLASS
        except:
            input_class = config.GITHUB_OAUTH_BUTTON_CLASS
    # set input button value
    if input_value == '':
        try:
            input_value = settings.GITHUB_OAUTH_BUTTON_VALUE
        except:
            input_value = config.GITHUB_OAUTH_BUTTON_VALUE
    # set input button id
    if input_id == '':
        try:
            input_id = settings.GITHUB_OAUTH_BUTTON_ID
        except:
            input_id = config.GITHUB_OAUTH_BUTTON_ID
    html_tag = '<input type="button" id="%s" value="%s" class="%s" onClick="location.href=\'%s\'">' % (input_id, input_value, input_class, api_url)
    return mark_safe(html_tag)
