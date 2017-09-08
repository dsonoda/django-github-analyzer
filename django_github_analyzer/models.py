from django.db import models
import json


class UserInfoQuerySet(models.query.QuerySet):
    """UserInfo QuerySet Class
    """
    def registered(self, login):
        """Confirm user's registration
        :param login: Github login value
        :return: True: registed / False: not registed
        """
        return self.filter(login=login, deleted=False)

    def registData(self, login, access_token, user_info):
        """Regist user data
        :param login (string): Github login
        :param access_token (string): Github application access token
        :param user_info (dict): Github other data
        :return:
        """
        return self.create(
            access_token=access_token,
            login=login,
            github_id=user_info['id'] if 'id' in user_info else '',
            html_url=user_info['html_url'] if 'html_url' in user_info else '',
            name=user_info['name'] if 'name' in user_info else '',
            email=user_info['email'] if 'email' in user_info else '',
            bio=user_info['bio'] if 'bio' in user_info else '',
            location=user_info['location'] if 'location' in user_info else '',
            company=user_info['company'] if 'company' in user_info else '',
            params=json.dumps(user_info)
        )

    def updateData(self, login, user_info):
        """Update user data
        :param login (string): Github login
        :param user_info (dict): Github other data
        :return:
        """
        s = self.get(login=login, deleted=False)
        if 'id' in user_info:
            s.github_id = user_info['id']
        if 'html_url' in user_info:
            s.html_url = user_info['html_url']
        if 'name' in user_info:
            s.name = user_info['name']
        if 'email' in user_info:
            s.email = user_info['email']
        if 'bio' in user_info:
            s.bio = user_info['bio']
        if 'location' in user_info:
            s.location = user_info['location']
        if 'company' in user_info:
            s.company = user_info['company']
        s.params = json.dumps(user_info)
        return s.save()

class UserInfoManager(models.Manager):
    """UserInfo Manager Class
    """
    def get_query_set(self):
        return UserInfoQuerySet(self.model)

    def registered(self, login):
        return self.get_query_set().registered(login)

    def registData(self, login, access_token, user_info):
        return self.get_query_set().registData(login, access_token, user_info)

    def updateData(self, login, user_info):
        return self.get_query_set().updateData(login, user_info)

class UserInfo(models.Model):
    """Github user information
    """
    # Github application access token
    access_token = models.CharField(null=False, max_length=100)
    # Github login
    login = models.CharField(null=False, max_length=100)
    # Github id
    github_id = models.IntegerField(null=True)
    # Github home url
    html_url = models.CharField(null=True, max_length=1000)
    # Github name
    name = models.CharField(null=True, max_length=255)
    # Github email
    email = models.CharField(null=True, max_length=255)
    # Github bio
    bio = models.TextField(null=True)
    # Github location
    location = models.CharField(null=True, max_length=255)
    # Github company
    company = models.CharField(null=True, max_length=255)
    # Github other data（format:JSON）
    params = models.TextField(null=True)
    # registed datetime
    created = models.DateTimeField(auto_now_add=True)
    """
    delete flg
        True: record used in the system
        False: record not used in the system
    """
    deleted = models.BooleanField(u'delete flg', default=False)

    # def __str__(self):
    #     return self.login

    objects = UserInfoManager()

class RepositoryQuerySet(models.query.QuerySet):
    """Repository QuerySet Class
    """
    def registered(self, user, name):
        """Confirm repository's registration
        :param user: Github user
        :param name: Github repository name
        :return: True: registed / False: not registed
        """
        return self.filter(user=user, name=name, deleted=False)

    def registData(self, user_info, name, repository_info):
        """Regist user data
        :param user_info : UserInfo
        :param name (string): Github repository name
        :param repository_info (dict): Github other data
        :return:
        """
        # raise Exception(repository_info['full_name'])
        return self.create(
            user=user_info,
            name=name,
            github_id=repository_info['id'] if 'id' in repository_info else '',
            full_name=repository_info['full_name'] if 'full_name' in repository_info else '',
            git_url=repository_info['git_url'] if 'git_url' in repository_info else '',
            ssh_url=repository_info['ssh_url'] if 'ssh_url' in repository_info else '',
            clone_url=repository_info['clone_url'] if 'clone_url' in repository_info else '',
            html_url=repository_info['html_url'] if 'html_url' in repository_info else '',
            language=repository_info['language'] if 'language' in repository_info else '',
            description=repository_info['description'] if 'description' in repository_info else '',
            private=repository_info['private'] if 'private' in repository_info else '',
            fork=repository_info['fork'] if 'fork' in repository_info else '',
            forks_count=repository_info['forks_count'] if 'forks_count' in repository_info else '',
            created_at=repository_info['created_at'] if 'created_at' in repository_info else '',
            updated_at=repository_info['updated_at'] if 'updated_at' in repository_info else '',
            params=json.dumps(repository_info)
        )

    def updateData(self, user, name, repository_info):
        """Update user data
        :param user : UserInfo
        :param name (string): Github repository name
        :param repository_info (dict): Github other data
        :return:
        """
        r = self.get(user=user, name=name, deleted=False)
        if 'github_id' in repository_info:
            r.github_id = repository_info['github_id']
        if 'full_name' in repository_info:
            r.full_name = repository_info['full_name']
        if 'git_url' in repository_info:
            r.git_url = repository_info['git_url']
        if 'ssh_url' in repository_info:
            r.ssh_url = repository_info['ssh_url']
        if 'clone_url' in repository_info:
            r.clone_url = repository_info['clone_url']
        if 'html_url' in repository_info:
            r.html_url = repository_info['html_url']
        if 'language' in repository_info:
            r.language = repository_info['language']
        if 'description' in repository_info:
            r.description = repository_info['description']
        if 'private' in repository_info:
            r.private = repository_info['private']
        if 'fork' in repository_info:
            r.fork = repository_info['fork']
        if 'forks_count' in repository_info:
            r.forks_count = repository_info['forks_count']
        if 'created_at' in repository_info:
            r.created_at = repository_info['created_at']
        if 'updated_at' in repository_info:
            r.updated_at = repository_info['updated_at']
        r.params = json.dumps(repository_info)
        return r.save()

class RepositoryManager(models.Manager):
    """Repository Manager Class
    """
    def get_query_set(self):
        return RepositoryQuerySet(self.model)

    def registered(self, user, name):
        return self.get_query_set().registered(user, name)

    def registData(self, user, name, repository_info):
        return self.get_query_set().registData(user, name, repository_info)

    def updateData(self, user, name, repository_info):
        return self.get_query_set().updateData(user, name, repository_info)

class Repository(models.Model):
    """Github repository information
        UserInfo:Repository=One:Many
    """
    # Github user
    user = models.ForeignKey(UserInfo, null=False, on_delete=models.CASCADE)
    # Repository name
    name = models.CharField(null=True, max_length=255)
    # Repository id
    github_id = models.IntegerField(null=True)
    # Repository full name
    full_name = models.CharField(null=True, max_length=255)
    # http git git url
    git_url = models.CharField(null=True, max_length=1000)
    # http git ssh url
    ssh_url = models.CharField(null=True, max_length=1000)
    # http git clone url
    clone_url = models.CharField(null=True, max_length=1000)
    # http git url
    html_url = models.CharField(null=True, max_length=1000)
    # programming language
    language = models.CharField(null=True, max_length=100)
    # Repository description
    description = models.TextField(null=True)
    # Whether this repository is private
    private = models.BooleanField(default=False)
    # Whether this repository is forking other repositories
    fork = models.BooleanField(default=False)
    # Repository forks count
    forks_count = models.IntegerField(null=True)
    # Repository create time
    created_at = models.DateTimeField(null=True)
    # Repository update time
    updated_at = models.DateTimeField(null=True)
    # Github other data（format:JSON）
    params = models.TextField(null=True)
    """
    delete flg
        True: record used in the system
        False: record not used in the system
    """
    deleted = models.BooleanField(u'delete flg', default=False)

    def __str__(self):
        return self.name

    objects = RepositoryManager()