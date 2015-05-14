from libsaas import http, parsers
from libsaas.services import base

from . import resource

class BranchesBase(resource.GitlabResource):
    path = 'repository/branches'

    @base.apimethod
    def protect(self):
        """
        Protect branch
        """
        url = '{0}/protect'.format(self.get_url())

        return http.Request('PUT', url), parsers.parse_json

    @base.apimethod
    def unprotect(self):
        """
        Unprotect branch
        """
        url = '{0}/unprotect'.format(self.get_url())

        return http.Request('PUT', url), parsers.parse_json

class Branch(BranchesBase):

    @base.apimethod
    def create(self, obj):
        raise base.MethodNotSupported()

    @base.apimethod
    def update(self, obj):
        raise base.MethodNotSupported()
