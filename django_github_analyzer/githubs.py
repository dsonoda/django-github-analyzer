"""
This module for getting information necessary for analysis from Github using the PyGithub module.
:see: https://github.com/PyGithub/PyGithub
      http://pygithub.readthedocs.io/en/latest/index.html
"""

from github import Github


class ModelGithub():
    """PyGithub wrapper module.
    """

    def __init__(self, access_token):
        """Initial settings.
        :param access_token (string): github application access token.
        """
        """
        Main class: Github
        http://pygithub.readthedocs.io/en/latest/github.html
        """
        self.main = Github(access_token)

        """
        AuthenticatedUser
        :see: http://pygithub.readthedocs.io/en/latest/github_objects/AuthenticatedUser.html
        """
        self.user = self.main.get_user()

        """
        Repositories Pagination
        :see: http://pygithub.readthedocs.io/en/latest/github_objects/AuthenticatedUser.html#github.AuthenticatedUser.AuthenticatedUser.get_repos
        """
        self.repositories = self.user.get_repos()

    def get_user_info(self):
        """Get user information.
        :return: dict
        """
        # github user informations
        # http://pygithub.readthedocs.io/en/latest/github_objects/AuthenticatedUser.html
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

    def get_repo_names(self):
        """Get repositories name.
        :return: list
        """
        names = []
        for repository in self.repositories:
            names.append(repository.name)
        return names

    def get_repo_info(self, repo_name):
        """Get repository information.
        :param repo_name (string): Repository name
        :return: dict
        """
        # github repository informations
        # http://pygithub.readthedocs.io/en/latest/github_objects/Repository.html
        repository = self.user.get_repo(repo_name)
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
