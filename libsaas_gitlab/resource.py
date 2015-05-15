from libsaas import http, parsers
from libsaas.services import base


def mimetype_accept(format):
    if not format:
        return {}
    mimetype = 'application/vnd.github.v3.{0}+json'.format(format)
    return {'Accept': mimetype}


def parse_boolean(body, code, headers):
    # The boolean value endpoints respond with 204 if the response is true and
    # 404 if it is not.
    if code == 204:
        return True
    if code == 404:
        return False
    raise http.HTTPError(body, code, headers)


class GitlabResource(base.RESTResource):

    @base.apimethod
    def get(self, data = None):
        """
        Get all data
        """
        request = http.Request('GET', self.get_url(), data)

        return request, parsers.parse_json

class MembersBase(GitlabResource):
    path = 'members'


class Members(MembersBase):

    @base.apimethod
    def update(self, obj):
        raise base.MethodNotSupported()

    @base.apimethod
    def delete(self):
        raise base.MethodNotSupported()

class Member(MembersBase):

    @base.apimethod
    def get(self):
        raise base.MethodNotSupported()

    @base.apimethod
    def create(self, obj):
        raise base.MethodNotSupported()

