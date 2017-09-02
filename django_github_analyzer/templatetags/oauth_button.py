from django import template
from django.utils.safestring import mark_safe
from django_github_analyzer import config

register = template.Library()

@register.assignment_tag
def oauth_button(api_url, input_class, input_value):
    """
    Output Github service collaboration button
    :param api_url: Github OAuth API URL (http://github.com/login/oauth/authorize) + query parameters
    :param input_class: Class name for button decoration
    :param input_value: Button word
    :return: html tag
    """
    if input_value == '':
        input_value = config.button_value
    if input_class == '':
        input_class = config.button_class
    html_tag = '<input type="button" value="%s" class="%s" onClick="location.href=\'%s\'">' % (input_value, input_class, api_url)
    return mark_safe(html_tag)
