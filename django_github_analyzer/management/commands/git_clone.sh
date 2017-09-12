#!/bin/bash
# mysite
export DJANGO_SETTINGS_MODULE=mysite.settings
# GITHUB APPLICATION SETTING
export GITHUB_OAUTH_CLIENT_ID=
export GITHUB_OAUTH_CLIENT_SECRET=
# SOURCE CODE PATH
export GITHUB_SRC_PATH=/vagrant/github_codes/

cmd="cd /vagrant"
eval ${cmd}

script1="source venv/bin/activate"
eval ${script1}

script2="python ./manage.py git_clone"
eval ${script2}