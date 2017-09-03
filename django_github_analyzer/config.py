"""Github About authorization options for OAuth Apps
https://developer.github.com/apps/building-integrations/setting-up-and-registering-oauth-apps/about-authorization-options-for-oauth-apps/
"""

"""OAuth authorization redirect uri.
https://developer.github.com/apps/building-integrations/setting-up-and-registering-oauth-apps/about-authorization-options-for-oauth-apps/#1-users-are-redirected-to-request-their-github-identity
"""
oauth_authorize_uri = 'http://github.com/login/oauth/authorize'

# OAuth button default value
button_value = 'Github OAuth'

# OAuth button default class name
button_class = 'square_btn'

"""Get access token uri
https://developer.github.com/apps/building-integrations/setting-up-and-registering-oauth-apps/about-authorization-options-for-oauth-apps/#2-users-are-redirected-back-to-your-site-by-github
"""
oauth_access_token_uri = 'https://github.com/login/oauth/access_token'

"""
get user information uri
    method: get
    https://developer.github.com/apps/building-integrations/setting-up-and-registering-oauth-apps/about-authorization-options-for-oauth-apps/#3-use-the-access-token-to-access-the-api
"""
get_user_information_uri = 'https://api.github.com/user'
