from __future__ import unicode_literals

from django.db import models
import base64

# Create your models here.


class PasswordManager(models.Manager):
    use_for_related_fields = True

    def create(self, *args, **kwargs):
        try:
            kwargs['password'] = base64.encodestring(kwargs['password'])
        except KeyError:
            pass

        return super(PasswordManager, self).create(*args, **kwargs)

    def get(self, *args, **kwargs):
        data = super(PasswordManager, self).get(*args, **kwargs)
        try:
            data.password = base64.decodestring(data.password)
        except AttributeError:
            pass
        return data


class UserProfile(models.Model):

    email = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    role = models.ManyToManyField('Role', through='UserRoles', related_name='roles')

    objects = PasswordManager()

    def __str__(self):
        return self.email


class Role(models.Model):

    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class UserRoles(models.Model):
    user = models.ForeignKey(UserProfile, related_name='userroles')
    role = models.ForeignKey(Role, related_name='userroles')

    def __str__(self):
        return '%s-%s' % (self.user, self.role)

