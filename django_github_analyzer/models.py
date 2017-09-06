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

    def registOrUpdateData(self, login, access_token, user_info):
        """Regist or update data
        :param login: Github login
        :param access_token: Github application access token
        :param user_info: Github other data（format:JSON）
        :return:
        """
        if self.registered(login).count() >= 1:
            # update
            s = self.get(login=login, deleted=False)
            s.access_token = access_token
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
        else:
            # insert
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
                params=json.dumps(user_info),
            )

class UserInfoManager(models.Manager):
    """UserInfo Manager Class
    """
    def get_query_set(self):
        return UserInfoQuerySet(self.model)

    def registered(self, login):
        return self.get_query_set().registered(login)

    def registOrUpdateData(self, login, access_token, user_info):
        return self.get_query_set().registOrUpdateData(login, access_token, user_info)

class UserInfo(models.Model):
    """Github user information
    """
    # Github application access token
    access_token = models.TextField(null=False)
    # Github login
    login = models.CharField(null=False, max_length=255)
    # Github id
    github_id = models.IntegerField(null=True)
    # Github home url
    html_url = models.TextField(null=True)
    # Github name
    name = models.CharField(null=True, max_length=255)
    # Github email
    email = models.CharField(null=True, max_length=255)
    # Github bio
    bio = models.TextField(null=True)
    # Github location
    location = models.CharField(null=True, max_length=255)
    # Github company
    company = models.TextField(null=True)
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
    pass