from libsaas import http, parsers
from libsaas.services import base

from . import resource
from . import notes

class MergeRequestsBase(resource.GitlabResource):
    path = 'merge_requests'

class MergeRequests(MergeRequestsBase):
    pass

class MergeRequestComments(MergeRequests):
    path = 'comments'

class MergeRequest(MergeRequests):
    
    path = 'merge_request'

    @base.apimethod
    def changes(self):
        """
        Fetch changes
        """
        url = '{0}/changes'.format(self.get_url())

        return http.Request('GET', url), parsers.parse_json

    @base.apimethod
    def accept(self, data = None):
        """
        Accept merge request
        """
        url = '{0}/merge'.format(self.get_url())

        return http.Request('PUT', url, data), parsers.parse_json

    @base.resource(notes.Note)
    def note(self, note_id):
        """
        Return a resource corresponding to a single note.
        """
        return notes.Note(self, note_id)

    @base.resource(notes.Notes)
    def notes(self):
        """
        Return a resource corresponding to all notes.
        """
        return notes.Notes(self)

    @base.resource(MergeRequestComments)
    def comments(self):
        """
        Return a resource corresponding to comments.
        """
        return MergeRequestComments(self)            


