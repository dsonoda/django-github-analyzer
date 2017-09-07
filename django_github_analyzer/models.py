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

    def __str__(self):
        return self.login

    objects = UserInfoManager()


class Repository(models.Model):
    """Github repository information
        UserInfo:Repository=One:Many
    """
    # Github user
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)



