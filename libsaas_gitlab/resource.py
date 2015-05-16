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

class NotesBase(base.RESTResource):
    path = 'notes'

class Notes(NotesBase):
    pass

class Note(NotesBase):
    pass

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

class LabelsBase(base.RESTResource):
    path = 'labels'

    @base.apimethod
    def update(self, obj):
        """
        Update object
        """
        url = '{0}'.format(self.get_url())

        return http.Request('PUT', url, obj), parsers.parse_json

    @base.apimethod
    def delete(self):
        """
        Delete
        """
        url = '{0}'.format(self.get_url())

        return http.Request('DELETE', url), parsers.parse_json

class MilestonesBase(GitlabResource):
    path = 'milestones'

    @base.apimethod
    def delete(self):
        raise base.MethodNotSupported()

class Milestones(MilestonesBase):

    @base.apimethod
    def update(self, obj):
        raise base.MethodNotSupported()

class Milestone(MilestonesBase):

    @base.apimethod
    def issues(self):
        """
        Issues resource
        """
        url = '{0}/issues'.format(self.get_url())

        return http.Request('GET', url), parsers.parse_json

class SnippetsBase(base.RESTResource):
    path = 'snippets'


class Snippets(SnippetsBase):

    @base.apimethod
    def delete(self):
        raise base.MethodNotSupported()

    @base.apimethod
    def update(self, obj):
        raise base.MethodNotSupported()

class Snippet(SnippetsBase):

    @base.apimethod
    def raw(self):
        """
        Raw content
        """
        url = '{0}/raw'.format(self.get_url())

        return http.Request('GET', url), parsers.parse_json

    @base.resource(Note)
    def note(self, note_id):
        """
        Return a resource corresponding to a single note.
        """
        return Note(self, note_id)

    @base.resource(Notes)
    def notes(self):
        """
        Return a resource corresponding to all notes.
        """
        return Notes(self)

class FilesBase(GitlabResource):
    path = 'files'

    @base.apimethod
    def create(self, data):
        """
        Update
        """
        url = '{0}'.format(self.get_url())
        return http.Request('POST', url, data), parsers.parse_json

    @base.apimethod
    def update(self, data):
        """
        Update
        """
        url = '{0}'.format(self.get_url())
        return http.Request('PUT', url, data), parsers.parse_json

    @base.apimethod
    def delete(self, data):
        """
        Delete
        """
        url = '{0}'.format(self.get_url())
        return http.Request('DELETE', url, data), parsers.parse_json

class ServicesBase(GitlabResource):
    path = 'services'

    @base.apimethod
    def get(self):
        raise base.MethodNotSupported()

    @base.apimethod
    def create(self, obj):
        raise base.MethodNotSupported()

class RepositoryBase(base.RESTResource):
    path = 'repository'

    @base.apimethod
    def tags(self):
        """
        Tags
        """
        url = '{0}/tags'.format(self.get_url())

        return http.Request('GET', url), parsers.parse_json

    @base.apimethod
    def tag(self, data):
        """
        Tag
        """
        url = '{0}/tags'.format(self.get_url())

        return http.Request('POST', url, data), parsers.parse_json

    @base.apimethod
    def tree(self):
        """
        Tree
        """
        url = '{0}/tree'.format(self.get_url())

        return http.Request('GET', url), parsers.parse_json

    @base.apimethod
    def raw_file(self, sha, data):
        """
        Raw file content
        """
        url = '{0}/blobs/{1}'.format(self.get_url(), sha)

        return http.Request('GET', url, data), parsers.parse_json

    @base.apimethod
    def raw_blob(self, sha):
        """
        Raw file content
        """
        url = '{0}/raw_blobs/{1}'.format(self.get_url(), sha)

        return http.Request('GET', url), parsers.parse_json

    @base.apimethod
    def get_archive(self):
        """
        Get archive
        """
        url = '{0}/archive'.format(self.get_url())

        return http.Request('GET', url), parsers.parse_json

    @base.apimethod
    def compare(self, data):
        """
        Compare
        """
        url = '{0}/compare'.format(self.get_url())

        return http.Request('GET', url, data), parsers.parse_json

    @base.apimethod
    def contributors(self):
        """
        Contributors
        """
        url = '{0}/contributors'.format(self.get_url())

        return http.Request('GET', url), parsers.parse_json

    @base.resource(FilesBase)
    def file(self):
        """
        Get files resource
        """
        return FilesBase(self)

class Session(GitlabResource):
    path = 'session'

    @base.apimethod
    def get(self):
        raise base.MethodNotSupported()

    @base.apimethod
    def update(self, obj):
        raise base.MethodNotSupported()

    @base.apimethod
    def delete(self):
        raise base.MethodNotSupported()

class HooksBase(base.RESTResource):
    path = 'hooks'

class Hooks(HooksBase):

    @base.apimethod
    def update(self, obj):
        raise base.MethodNotSupported()

    @base.apimethod
    def delete(self):
        raise base.MethodNotSupported()

class Hook(HooksBase):

    @base.apimethod
    def test(self):
        """
        Test hook
        """
        return http.Request('GET', self.get_url()), parsers.parse_json

    @base.apimethod
    def update(self, obj):
        raise base.MethodNotSupported()

    @base.apimethod
    def create(self, obj):
        raise base.MethodNotSupported()
