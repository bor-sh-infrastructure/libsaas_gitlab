from libsaas import http, parsers
from libsaas.services import base

from . import resource

class UserKeys(resource.GitlabResource):
    path = 'keys'

class UsersBase(resource.GitlabResource):
    path = 'users'

    @base.resource(UserKeys)
    def keys(self):
        """
        Return the resource corresponding to all keys.
        """
        return UserKeys(self)

class CurrentUser(UsersBase):
    path = 'user'

class User(UsersBase):
    path = 'users'

class Users(UsersBase):
    path = 'users'

    @base.apimethod
    def get(self, search=None, page=None, per_page=None):
        """
        Get users.

        :var search: search string
        :vartype search: str
        :var page: one page found
        :vartype page: int
        :var per_page: number of findings pro page 
        :vartype per_page: int
        """
        params = base.get_params(('search', 'page', 'per_page'), locals())
        url    = self.get_url()

        return http.Request('GET', url, params), parsers.parse_json
