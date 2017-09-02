"""
Github OAuth Settings (without credential informations)
https://developer.github.com/apps/building-integrations/setting-up-and-registering-oauth-apps/about-authorization-options-for-oauth-apps/
"""

"""
oauth/authorize uri
    method: get
    https://developer.github.com/apps/building-integrations/setting-up-and-registering-oauth-apps/about-authorization-options-for-oauth-apps/#1-users-are-redirected-to-request-their-github-identity
"""
oauth_authorize_uri = 'http://github.com/login/oauth/authorize'

"""
oauth/access_token uri
    method: post
    https://developer.github.com/apps/building-integrations/setting-up-and-registering-oauth-apps/about-authorization-options-for-oauth-apps/#2-users-are-redirected-back-to-your-site-by-github
"""
oauth_access_token_uri = 'https://github.com/login/oauth/access_token'

"""
get user information uri
    method: get
    https://developer.github.com/apps/building-integrations/setting-up-and-registering-oauth-apps/about-authorization-options-for-oauth-apps/#3-use-the-access-token-to-access-the-api
"""
get_user_information_uri = 'https://api.github.com/user'

# django application callback url
django_callback_url = '/django_github_analyzer/oauth_callback/'

# OAuth button value
button_value = 'Github OAuth'

# OAuth button class name
button_class = 'square_btn'

"""
oauth scope
    delimiters: space
    https://developer.github.com/apps/building-integrations/setting-up-and-registering-oauth-apps/about-scopes-for-oauth-apps/
"""
# scope = 'user public_repo gist'
scope = ''
