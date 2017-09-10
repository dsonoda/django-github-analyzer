from django.db import models
from django_github_analyzer import config
import json
import datetime
import time


class UserInfoQuerySet(models.query.QuerySet):
    """UserInfo QuerySet Class
    """
    def registered(self, login):
        """Confirm user's registration
        :param login: Github login value
        :return: True: registed / False: not registed
        """
        return self.filter(login=login, deleted=False)

    def regist_data(self, login, access_token, user_info):
        """Regist user data
        :param login (string): Github login
        :param access_token (string): Github application access token
        :param user_info (dict): Github other data
        :return (boolean): True:success / False:failed
        """
        if self.registered(login).count() == 0:
            self.create(
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
            return True
        else:
            return False

    def update_data(self, login, user_info):
        """Update user data
        :param login (string): Github login
        :param user_info (dict): Github other data
        :return (boolean): True:success / False:failed
        """
        if self.registered(login).count() == 0:
            return False
        else:
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
            s.save()
            return True

    def get_param_value(self, param_name, login):
        """Get Value from 'param' column values
        :param param_name (string):
        :param login (string): UserInfo.login
        :return (string): parameter value
        """
        params = self.get(login=login).params
        params = json.loads(params)
        return params[param_name] if param_name in params else None

class UserInfoManager(models.Manager):
    """UserInfo Manager Class
    """
    def get_query_set(self):
        return UserInfoQuerySet(self.model)

    def registered(self, login):
        return self.get_query_set().registered(login)

    def regist_data(self, login, access_token, user_info):
        return self.get_query_set().regist_data(login, access_token, user_info)

    def update_data(self, login, user_info):
        return self.get_query_set().update_data(login, user_info)

    def get_param_value(self, param_name, login):
        return self.get_query_set().get_param_value(param_name, login)

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
    """delete flg
        True: record not used in the system
        False: record used in the system
    """
    deleted = models.BooleanField(u'delete flg', default=False)

    objects = UserInfoManager()

    def __str__(self):
        return self.name

class RepositoryQuerySet(models.query.QuerySet):
    """Repository QuerySet Class
    """
    def registered(self, user_info, name):
        """Confirm repository's registration
        :param user_info: Github user
        :param name: Github repository name
        :return: True: registed / False: not registed
        """
        return self.filter(user_info=user_info, name=name, deleted=False)

    def regist_data(self, user_info, name, repository_info):
        """Regist user data
        :param user_info : UserInfo
        :param name (string): Github repository name
        :param repository_info (dict): Github other data
        :return (boolean): True:success / False:failed
        """
        if self.registered(user_info, name).count() == 0:
            self.create(
                user_info=user_info,
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
            return True
        else:
            return False

    def update_data(self, user_info_login, name, repository_info):
        """Update user data
        :param user_info_login : UserInfo.login
        :param name (string): Github repository name
        :param repository_info (dict): Github other data
        :return (boolean): True:success / False:failed
        """
        user_info = UserInfo.objects.get(login=user_info_login, deleted=False)
        if self.registered(user_info, name).count() == 0:
            return False
        else:
            r = self.get(user_info__login=user_info_login, name=name, deleted=False)
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
            if 'clone_at' in repository_info:
                r.clone_at = repository_info['clone_at']
            if 'pull_at' in repository_info:
                r.pull_at = repository_info['pull_at']
            r.params = json.dumps(repository_info)
            if 'analysis_result' in repository_info:
                r.analysis_result = json.dumps(repository_info['analysis_result'])
            r.save()
            return True

    def get_param_value(self, param_name, user_info_login, name):
        """Get Value from 'param' column values
        :param param_name (string):
        :param user_info_login (string): UserInfo.login
        :param name (string): repository name
        :return (string): parameter value
        """
        params = self.get(user_info__login=user_info_login, name=name).params
        params = json.loads(params)
        return params[param_name] if param_name in params else None

    def get_analysis_value(self, analysis_name, user_info_login, name):
        """Get Value from 'analysis_result' column values
        :param analysis_name (string):
        :param user_info_login (string): UserInfo.login
        :param name (string): repository name
        :return (string): analysis_result parameter value
        """
        analysis_result = self.get(user_info__login=user_info_login, name=name).analysis_result
        analysis_result = json.loads(analysis_result)
        return analysis_result[analysis_name] if analysis_name in analysis_result else None

    def is_clone(self, user_info_login, name):
        """Confirm already git clone repository
        :param user_info_login : UserInfo.login
        :param name (string): Github repository name
        :return (boolean): True:already clone / False not clone
        """
        user_info = UserInfo.objects.get(login=user_info_login, deleted=False)
        if self.registered(user_info, name).count() == 0:
            return False
        elif self.filter(user_info=user_info, name=name).exclude(clone_at=None).count() == 0:
            return False
        else:
            return True

    def regist_git_clone_at(self, user_info_login, name):
        """Regist clone_at and pull_at
        :param user_info_login : UserInfo.login
        :param name (string): Github repository name
        :return (boolean): True:success / False:failed
        """
        date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        repository_info = {
            "clone_at": date_time,
            "pull_at": date_time,
        }
        return self.update_data(user_info_login, name, repository_info)

class RepositoryManager(models.Manager):
    """Repository Manager Class
    """
    def get_query_set(self):
        return RepositoryQuerySet(self.model)

    def registered(self, user_info, name):
        return self.get_query_set().registered(user_info, name)

    def regist_data(self, user_info, name, repository_info):
        return self.get_query_set().regist_data(user_info, name, repository_info)

    def update_data(self, user_info_login, name, repository_info):
        return self.get_query_set().update_data(user_info_login, name, repository_info)

    def get_param_value(self, param_name, user_info_login, name):
        return self.get_query_set().get_param_value(param_name, user_info_login, name)

    def get_analysis_value(self, analysis_name, user_info_login, name):
        return self.get_query_set().get_analysis_value(analysis_name, user_info_login, name)

    def is_clone(self, user_info_login, name):
        return self.get_query_set().is_clone(user_info_login, name)

    def regist_git_clone_at(self, user_info_login, name):
        return self.get_query_set().git_clone(user_info_login, name)

class Repository(models.Model):
    """Github repository information
        UserInfo:Repository=One:Many
    """
    # Github user
    user_info = models.ForeignKey(UserInfo, null=False, on_delete=models.CASCADE)
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
    # Git clone date from Github
    clone_at = models.DateTimeField(null=True)
    # Git pull date from Github
    pull_at = models.DateTimeField(null=True)
    # Github other data（format:JSON）
    params = models.TextField(null=True)
    # Analyzed result values（format:JSON）
    analysis_result = models.TextField(null=True)
    """delete flg
        True: record not used in the system
        False: record used in the system
    """
    deleted = models.BooleanField(u'delete flg', default=False)

    objects = RepositoryManager()

    def __str__(self):
        return self.full_name

class TaskQuerySet(models.query.QuerySet):
    """Task QuerySet Class
    """
    def get_status(self, mode, **args):
        """
        Get Task status
        :param mode (integer): see: config.TASK_MODE_CHOICES
        :param args (dict): key is 'queue_id' or ('user_info_login' and 'repository_name')
        :return (integer): config.TASK_STATUS_CHOICES key
        """
        obj = self.filter(mode=mode, deleted=False)
        if 'queue_id' in args:
            obj.filter(queue_id=args['queue_id'])
        elif 'user_info_login' in args and 'repository_name' in args:
            obj.filter(user_info__login=args['user_info_login'], repository__name=args['repository_name'])
        else:
            raise Exception('Required argument is missing.')
        return obj.values('status')[0]['status']

class TaskManager(models.Manager):
    """Task Manager Class
    """
    def get_queryset(self):
        return TaskQuerySet(self.model, using=self._db)

    def get_status(self, mode, **args):
        return self.get_queryset().get_status(mode, args)

class Task(models.Model):
    """Task information
    """
    # SyncStatus.queue_id
    queue_id = models.CharField(null=False, max_length=50)
    # task status
    status = models.IntegerField(null=False, choices=config.TASK_STATUS_CHOICES)
    # Task mode
    mode = models.IntegerField(null=False, choices=config.TASK_MODE_CHOICES)
    # Github user
    user_info = models.ForeignKey(UserInfo, null=True, on_delete=models.CASCADE)
    # Github Repository
    repository = models.ForeignKey(Repository, null=True, on_delete=models.CASCADE)
    # start datetime
    start = models.DateTimeField(auto_now_add=True)
    # end datetime
    end = models.DateTimeField(null=True, blank=True)
    """delete flg
        True: record not used in the system
        False: record used in the system
    """
    deleted = models.BooleanField(u'delete flg', default=False)

    objects = TaskManager()

    def __str__(self):
        return self.name

    @classmethod
    def get_queue_id(cls):
        """generate queue id
        :return (string):
        """
        timestamp = time.time()
        timestamp = str(timestamp)
        m = md5()
        m.update(timestamp.encode())
        return m.hexdigest()
