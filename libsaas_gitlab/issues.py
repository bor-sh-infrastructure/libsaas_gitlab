from libsaas import http, parsers
from libsaas.services import base

from . import resource
from . import notes

class IssuesBase(resource.GitlabResource):
    path = 'issues'

    @base.apimethod
    def delete(self):
        raise base.MethodNotSupported()

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

class Issues(IssuesBase):

    @base.apimethod
    def create(self, obj):
        raise base.MethodNotSupported()

    @base.apimethod
    def update(self, obj):
        raise base.MethodNotSupported()

class ProjectIssues(IssuesBase):

    @base.apimethod
    def update(self, obj):
        raise base.MethodNotSupported()

class ProjectIssue(IssuesBase):

    @base.apimethod
    def create(self, obj):
        raise base.MethodNotSupported()

