from libsaas import http, parsers
from libsaas.services import base

class NotesBase(base.RESTResource):

    path = 'notes'

class Notes(NotesBase):
    pass

class Note(NotesBase):
    pass
