"""Github About authorization options for OAuth Apps
https://developer.github.com/apps/building-integrations/setting-up-and-registering-oauth-apps/about-authorization-options-for-oauth-apps/
"""

"""OAuth authorization redirect uri.
https://developer.github.com/apps/building-integrations/setting-up-and-registering-oauth-apps/about-authorization-options-for-oauth-apps/#1-users-are-redirected-to-request-their-github-identity
"""
OAUTH_AUTHORIZE_URI = 'http://github.com/login/oauth/authorize'

# OAuth button class name
GITHUB_OAUTH_BUTTON_CLASS = 'square_btn'

# OAuth button input value
GITHUB_OAUTH_BUTTON_VALUE = 'Github OAuth'

# OAuth button input id
GITHUB_OAUTH_BUTTON_ID = 'github_oauth'

"""Get access token uri
https://developer.github.com/apps/building-integrations/setting-up-and-registering-oauth-apps/about-authorization-options-for-oauth-apps/#2-users-are-redirected-back-to-your-site-by-github
"""
OAUTH_ACCESS_TOKEN_URI = 'https://github.com/login/oauth/access_token'

"""task status
"""
TASK_STATUS_ISSUED = 1
TASK_STATUS_START = 2
TASK_STATUS_END = 3
# model choices
TASK_STATUS_CHOICES = (
    (TASK_STATUS_ISSUED, 'Queue issued'),
    (TASK_STATUS_START, 'prosecc start'),
    (TASK_STATUS_END, 'prosecc end'),
)
# choices
TASK_STATUS = {
    TASK_STATUS_ISSUED: 'Queue issued',
    TASK_STATUS_START: 'prosecc start',
    TASK_STATUS_END: 'prosecc end',
}

"""task mode
"""
TASK_MODE_GIT_CLONE = 1
TASK_MODE_GIT_PULL = 2
TASK_MODE_CODE_ANALYZE = 3
# model choices
TASK_MODE_CHOICES = (
    (TASK_MODE_GIT_CLONE, 'Git clone'),
    (TASK_MODE_GIT_PULL, 'Git pull'),
    (TASK_MODE_CODE_ANALYZE, 'analyze source code'),
)
# choices
TASK_MODE = {
    TASK_MODE_GIT_CLONE: 'Git clone',
    TASK_MODE_GIT_PULL: 'Git pull',
    TASK_MODE_CODE_ANALYZE: 'analyze source code',
}
