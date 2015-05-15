from libsaas import http, parsers
from libsaas.services import base

from . import resource

class GroupsBase(resource.GitlabResource):
    path = 'groups'

    @base.apimethod
    def update(self, obj):
        raise base.MethodNotSupported()


class Groups(GroupsBase):

    @base.apimethod
    def search(self, search_string):
        """
        Search for groups
        """
        params = { "search":search_string }
        url    = self.get_url()

        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def delete(self):
        raise base.MethodNotSupported()

class Group(GroupsBase):

    @base.apimethod
    def transfer_project(self, project_id):
        """
        Transfer project to group
        """
        url = '{0}/projects/{1}'.format(self.get_url(), project_id)

        return http.Request('POST', url), parsers.parse_json

    @base.resource(resource.Members)
    def members(self):
        """
        Get members
        """
        return resource.Members(self)

    @base.resource(resource.Member)
    def member(self, user_id):
        """
        Get team member by id
        """
        return resource.Member(self, user_id)

    @base.apimethod
    def create(self, obj):
        raise base.MethodNotSupported()

    @base.apimethod
    def update(self, obj):
        raise base.MethodNotSupported()
