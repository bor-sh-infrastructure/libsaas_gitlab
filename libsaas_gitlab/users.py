from libsaas import http, parsers
from libsaas.services import base

from . import resource
from . import keys

class UsersBase(resource.GitlabResource):
    path = 'users'

    @base.resource(keys.Key)
    def key(self, key_id):
        """
        Return a key resource.
        """
        return keys.Key(self, key_id)

    @base.resource(keys.Keys)
    def keys(self):
        """
        Return all keys resource.
        """
        return keys.Keys(self)

class CurrentUser(UsersBase):
    path = 'user'

    @base.apimethod
    def create(self, obj):
        raise base.MethodNotSupported()

class User(UsersBase):
    path = 'users'

class Users(UsersBase):
    path = 'users'