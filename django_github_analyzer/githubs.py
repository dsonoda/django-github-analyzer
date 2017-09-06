import os
import urllib.parse
import requests
from github import Github
from django_github_analyzer import config


class ModelGithub():
    """PyGithub wrapper module.
    """

    def __init__(self, access_token):
        """Initial settings.
        :param access_token (string): github application access token.
        """
        # set PyGithub object
        self.main = Github(access_token)
        self.user = self.main.get_user()

    def get_user_info(self):
        """Get user information.
        :return: dict
        """
        return {
            'avatar_url': self.user.avatar_url,
            'bio': self.user.bio,
            'blog': self.user.blog,
            'collaborators': self.user.collaborators,
            'company': self.user.company,
            'created_at': str(self.user.created_at),
            'disk_usage': self.user.disk_usage,
            'email': self.user.email,
            'events_url': self.user.events_url,
            'followers': self.user.followers,
            'followers_url': self.user.followers_url,
            'following': self.user.following,
            'following_url': self.user.following_url,
            'gists_url': self.user.gists_url,
            'gravatar_id': self.user.gravatar_id,
            'hireable': self.user.hireable,
            'html_url': self.user.html_url,
            'id': self.user.id,
            'location': self.user.location,
            'login': self.user.login,
            'name': self.user.name,
            'organizations_url': self.user.organizations_url,
            'owned_private_repos': self.user.owned_private_repos,
            'private_gists': self.user.private_gists,
            'public_gists': self.user.public_gists,
            'public_repos': self.user.public_repos,
            'received_events_url': self.user.received_events_url,
            'repos_url': self.user.repos_url,
            'starred_url': self.user.starred_url,
            'subscriptions_url': self.user.subscriptions_url,
            'total_private_repos': self.user.total_private_repos,
            'updated_at': str(self.user.updated_at),
            'url': self.user.url,
        }
