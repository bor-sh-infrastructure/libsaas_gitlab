from libsaas import http, parsers
from libsaas.services import base

from . import resource

class IssuesBase(resource.GitlabResource):
    path = 'issues'

    @base.apimethod
    def delete(self):
        raise base.MethodNotSupported()

    @base.resource(resource.Note)
    def note(self, note_id):
        """
        Return a resource corresponding to a single note.
        """
        return resource.Note(self, note_id)

    @base.resource(resource.Notes)
    def notes(self):
        """
        Return a resource corresponding to all notes.
        """
        return resource.Notes(self)

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

