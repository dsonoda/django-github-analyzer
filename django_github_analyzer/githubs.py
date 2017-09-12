"""
This module for getting information necessary for analysis from Github using the PyGithub module.
:see: https://github.com/PyGithub/PyGithub
      http://pygithub.readthedocs.io/en/latest/index.html
"""

import os
import subprocess
from django_github_analyzer import config
from django.conf import settings
from github import Github


class ModelGithub():
    """PyGithub wrapper module.
    """

    """Absolute path of directory of local environment for storing Github's source code.
    If not specified, use environment information about .bashrc (GITHUB_SRC_PATH)
    """
    github_src_path = None

    def __init__(self, **args):
        """Initial settings.
        :param args:
            access_token (string): github application access token.
            private (boolean): Whether to process private repositories
            fork (boolean): Whether to process fork repositories
            github_src_path (string): github source code save path.
        """

        """Main class: Github
        :see: http://pygithub.readthedocs.io/en/latest/github.html
        """
        self.main = None

        # Whether to process private repositories
        self.__set_private(config.GITHUB_TARGET_REPO_PRIVATE)
        try:
            self.__set_private(settings.GITHUB_OAUTH_CALLBACK_URI)
        except:
            pass

        # Whether to process fork repositories
        self.__set_fork(config.GITHUB_TARGET_REPO_FORK)
        try:
            self.__set_fork(settings.GITHUB_TARGET_REPO_FORK)
        except:
            pass

        # set github src path
        if os.environ.get('GITHUB_SRC_PATH') != None:
            self.set_github_src_path(os.environ.get('GITHUB_SRC_PATH'))

        for key in args:
            if key == 'github_src_path':
                self.set_github_src_path(args[key])
            if key == 'access_token':
                self.__set_access_token(args[key])
            if key == 'private':
                self.__set_private(args[key])
            if key == 'fork':
                self.__set_fork(args[key])

        if self.get_github_src_path() == None:
            # src path from Github is required!
            raise Exception('Required argument is missing.')

    def isset_access_token(self):
        """Is set access token
        :return (boolean):
        """
        if self.main is not None:
            return True
        else:
            return False

    def __set_access_token(self, access_token=None):
        """Set access token and Github objects
        :param access_token (string): user access token
        :return:
        """
        if access_token is not None:
            self.main = Github(access_token)
        elif self.isset_access_token() == False:
            raise Exception('Required argument is missing.')

    def __set_private(self, private):
        """Set private
        :param private
        :return:
        """
        self.private = private

    def get_private(self):
        """Get private
        :return (boolean):
        """
        return self.private

    def __set_fork(self, fork):
        """Set fork
        :param fork
        :return:
        """
        self.fork = fork

    def get_fork(self):
        """Get fork
        :return (boolean):
        """
        return self.fork

    def set_github_src_path(self, github_src_path):
        """Setter github src path.
        :param github_src_path (string): Absolute path of directory of local environment for storing Github's source code.
        """
        self.github_src_path = '/' + github_src_path.strip('/') + '/'

    def get_github_src_path(self):
        """Getter github src path.
        :return: string
        """
        return self.github_src_path

    def get_user_info(self, access_token=None):
        """Get user information.
        :param access_token (string): user access token
        :return: dict
        """
        self.__set_access_token(access_token)

        """AuthenticatedUser
        :see: http://pygithub.readthedocs.io/en/latest/github_objects/AuthenticatedUser.html
        """
        user = self.main.get_user()

        # github user informations
        # http://pygithub.readthedocs.io/en/latest/github_objects/AuthenticatedUser.html
        return {
            'avatar_url': user.avatar_url,
            'bio': user.bio,
            'blog': user.blog,
            'collaborators': user.collaborators,
            'company': user.company,
            'created_at': str(user.created_at),
            'disk_usage': user.disk_usage,
            'email': user.email,
            'events_url': user.events_url,
            'followers': user.followers,
            'followers_url': user.followers_url,
            'following': user.following,
            'following_url': user.following_url,
            'gists_url': user.gists_url,
            'gravatar_id': user.gravatar_id,
            'hireable': user.hireable,
            'html_url': user.html_url,
            'id': user.id,
            'location': user.location,
            'login': user.login,
            'name': user.name,
            'organizations_url': user.organizations_url,
            'owned_private_repos': user.owned_private_repos,
            'private_gists': user.private_gists,
            'public_gists': user.public_gists,
            'public_repos': user.public_repos,
            'received_events_url': user.received_events_url,
            'repos_url': user.repos_url,
            'starred_url': user.starred_url,
            'subscriptions_url': user.subscriptions_url,
            'total_private_repos': user.total_private_repos,
            'updated_at': str(user.updated_at),
            'url': user.url,
        }

    def get_repository_names(self, access_token=None):
        """Get repositories name.
        :param access_token (string): user access token
        :return: list
        """
        self.__set_access_token(access_token)

        """Repositories Pagination
        :see: http://pygithub.readthedocs.io/en/latest/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.get_repos
        """
        names = []
        repositories = self.main.get_user().get_repos()
        for repository in repositories:
            if self.filter_repository_info(private=repository.private, fork=repository.fork):
                names.append(repository.name)
        return names

    def filter_repository_info(self, **args):
        """Filter repository informations handled by the system
        :param args:
            'private' (boolean): Whether to process private repositories
            'fork' (boolean): Whether to process fork repositories
        :return (boolean): True: OK / False: No!
        """
        # Do not process private repository
        if self.get_private() == False and ('private' in args and args['private'] == True):
            return False
        # Do not process fork repository
        if self.get_fork() == False and ('fork' in args and args['fork'] == True):
            return False
        return True

    def get_repository_info(self, repository_name, access_token=None):
        """Get repository information.
        :param repository_name:
        :param access_token (string): user access token
        :return: dict
        """
        self.__set_access_token(access_token)

        """github repository informations
        :see: http://pygithub.readthedocs.io/en/latest/github_objects/Repository.html
        """
        repository = self.main.get_user().get_repo(repository_name)
        information = {
            'archive_url': repository.archive_url,
            'assignees_url': repository.assignees_url,
            'blobs_url': repository.blobs_url,
            'branches_url': repository.branches_url,
            'clone_url': repository.clone_url,
            'collaborators_url': repository.collaborators_url,
            'comments_url': repository.comments_url,
            'commits_url': repository.commits_url,
            'compare_url': repository.compare_url,
            'contents_url': repository.contents_url,
            'contributors_url': repository.contributors_url,
            'created_at': str(repository.created_at),
            'default_branch': repository.default_branch,
            'description': repository.description,
            'downloads_url': repository.downloads_url,
            'events_url': repository.events_url,
            'fork': repository.fork,
            'forks': repository.forks,
            'forks_count': repository.forks_count,
            'forks_url': repository.forks_url,
            'full_name': repository.full_name,
            'git_commits_url': repository.git_commits_url,
            'git_refs_url': repository.git_refs_url,
            'git_tags_url': repository.git_tags_url,
            'git_url': repository.git_url,
            'has_downloads': repository.has_downloads,
            'has_issues': repository.has_issues,
            'has_wiki': repository.has_wiki,
            'homepage': repository.homepage,
            'hooks_url': repository.hooks_url,
            'html_url': repository.html_url,
            'id': repository.id,
            'issue_comment_url': repository.issue_comment_url,
            'issue_events_url': repository.issue_events_url,
            'issues_url': repository.issues_url,
            'keys_url': repository.keys_url,
            'labels_url': repository.labels_url,
            'language': repository.language,
            'languages_url': repository.languages_url,
            'master_branch': repository.master_branch,
            'merges_url': repository.merges_url,
            'milestones_url': repository.milestones_url,
            'mirror_url': repository.mirror_url,
            'name': repository.name,
            'network_count': repository.network_count,
            'notifications_url': repository.notifications_url,
            'open_issues': repository.open_issues,
            'open_issues_count': repository.open_issues_count,
            'private': repository.private,
            'pulls_url': repository.pulls_url,
            'pushed_at': str(repository.pushed_at),
            'size': repository.size,
            'ssh_url': repository.ssh_url,
            'stargazers_count': repository.stargazers_count,
            'stargazers_url': repository.stargazers_url,
            'statuses_url': repository.statuses_url,
            'subscribers_url': repository.subscribers_url,
            'subscription_url': repository.subscription_url,
            'svn_url': repository.svn_url,
            'tags_url': repository.tags_url,
            'teams_url': repository.teams_url,
            'trees_url': repository.trees_url,
            'updated_at': str(repository.updated_at),
            'url': repository.url,
            'watchers': repository.watchers,
            'watchers_count': repository.watchers_count,
        }
        return information

    def git_clone(self, git_url, user_info_login, repository_name):
        """Git clone from Github
        :param git_url: clone url
        :param user_info_login : UserInfo.login
        :param repository_name: Repository.name
        :return (boolean): True: success / False: failed
        """
        user_dir = self.get_github_src_path() + user_info_login + '/'
        save_path = user_dir + repository_name
        try:
            os.makedirs(user_dir, mode=0o777, exist_ok=True)
            subprocess.run(["git", "clone", git_url, save_path], check=True)
            return True
        except subprocess.CalledProcessError as e:
            return False

    def get_repository_info_value(self, param_name, repository_name, access_token=None):
        """Get Value from Git repository information
        :param param_name (string):
        :param repository_name (string): Repository name
        :param access_token (string): user access token
        :return (string): parameter value
        """
        self.__set_access_token(access_token)
        repository_information = self.get_repository_info(repository_name)
        return repository_information[param_name] if param_name in repository_information else None
