from libsaas import http, parsers
from libsaas.services import base

from . import resource

class CommitsBase(resource.GitlabResource):
    path = 'repository/commits'

    @base.apimethod
    def get_diff(self):
        """
        Get diff
        """
        url = '{0}/{1}/diff'.format(self.parent.get_url() + "/" + self.path, self.object_id)

        return http.Request('GET', url), parsers.parse_json

    @base.apimethod
    def get_comments(self):
        """
        Get comments
        """
        url = '{0}/{1}/comments'.format(self.parent.get_url() + "/" + self.path, self.object_id)

        return http.Request('GET', url), parsers.parse_json

    @base.apimethod
    def post_comment(self, data):
        """
        Post comment
        """
        url = '{0}/{1}/comments'.format(self.parent.get_url() + "/" + self.path, self.object_id)

        return http.Request('POST', url, data), parsers.parse_json

    @base.apimethod
    def create(self, obj):
        raise base.MethodNotSupported()

    @base.apimethod
    def delete(self):
        raise base.MethodNotSupported()

class Commit(CommitsBase):

    @base.apimethod
    def create(self, obj):
        raise base.MethodNotSupported()

    @base.apimethod
    def update(self, obj):
        raise base.MethodNotSupported()
