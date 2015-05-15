from libsaas import http, parsers
from libsaas.services import base

from . import resource

class KeysBase(resource.GitlabResource):
    path = 'keys'

    @base.apimethod
    def update(self, obj):
        raise base.MethodNotSupported()

class Keys(KeysBase):

    @base.apimethod
    def delete(self):
        raise base.MethodNotSupported()

class Key(KeysBase):

    @base.apimethod
    def create(self, obj):
        raise base.MethodNotSupported()
