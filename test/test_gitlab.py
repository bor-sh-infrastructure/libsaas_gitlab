import json
import unittest

from libsaas import port
from libsaas.services.base import MethodNotSupported
from libsaas.executors import test_executor
from libsaas.services import base
import libsaas_gitlab as gitlab

class GitlabTestCase(unittest.TestCase):

    def setUp(self):
        self.executor = test_executor.use()
        self.executor.set_response(b'{}', 200, {})

        self.service = gitlab.Gitlab("https://gitlab.com", 'my-token')

    def expect(self, method=None, uri=None, params=None, headers=None):
        if method:
            self.assertEqual(method, self.executor.request.method)
        if uri:
            self.assertEqual(self.executor.request.uri,
                              'https://gitlab.com/api/v3' + uri)
        if params:
            self.assertEqual(self.executor.request.params, params)
        if headers:
            self.assertEqual(self.executor.request.headers, headers)

    def test_auth(self):
        service = gitlab.Gitlab("https://gitlab.com", 'a-token')
        service.user().get()
        self.expect('GET', '/user', {}, {'PRIVATE-TOKEN': 'a-token'})

        service = gitlab.Gitlab("https://gitlab.com", 'token', 'oauth-token')
        service.user().get()
        self.expect('GET', '/user', {}, {'Authorization': 'Bearer oauth-token'})

    def test_projects(self):
        self.service.projects().get()
        self.expect('GET', '/projects')

        self.service.projects().get({ 'page':1, 'per_page':100 })
        self.expect('GET', '/projects', { 'page':1, 'per_page':100 })

        self.service.projects().get({ 'owned_or_all':'all' })
        self.expect('GET', '/projects/all', {})

        self.service.projects().get({ 'owned_or_all':'owned' })
        self.expect('GET', '/projects/owned', {})

        self.service.projects().search("name")
        self.expect('GET', '/projects/search/name')

        self.service.project(1).events()
        self.expect('GET', '/projects/1/events')

        self.service.project("namespace/rep").events()
        self.expect('GET', '/projects/namespace/rep/events')

        data = { 'name' : 'beautiful project' }
        self.service.projects().create(data)
        self.expect('POST', '/projects', data)

        with port.assertRaises(MethodNotSupported):
            self.service.projects().update(data)
        with port.assertRaises(MethodNotSupported):
            self.service.projects().delete()

        data = { 'name' : 'beautiful project' }
        self.service.projects().create_for_user(1, data)
        self.expect('POST', '/projects/user/1', data)

        data = { 'name' : 'beautiful project update' }
        self.service.project(1).update(data)
        self.expect('PUT', '/projects/1', data)

        self.service.project(1).fork()
        self.expect('POST', '/projects/fork/1')

        self.service.project(1).add_fork_relation(2)
        self.expect('POST', '/projects/1/fork/2')

        self.service.project(1).delete_fork_relation()
        self.expect('DELETE', '/projects/1/fork')

        self.service.project(1).delete()
        self.expect('DELETE', '/projects/1')

        #### Members

        self.service.project(1).members().get()
        self.expect('GET', '/projects/1/members')

        self.service.project(1).member(2).get()
        self.expect('GET', '/projects/1/members/2')

        data = { 'test' : 'test' }
        self.service.project(1).members().create(data)
        self.expect('POST', '/projects/1/members')

        with port.assertRaises(MethodNotSupported):
            self.service.project(1).members().update(data)
        with port.assertRaises(MethodNotSupported):
            self.service.project(1).members().delete()

        data = { 'test' : 'test' }
        self.service.project(1).member(2).update(data)
        self.expect('PUT', '/projects/1/members/2')

        self.service.project(1).member(2).delete()
        self.expect('DELETE', '/projects/1/members/2')

        ##### Hooks

        self.service.project(1).hooks().get()
        self.expect('GET', '/projects/1/hooks')

        self.service.project(1).hook(2).get()
        self.expect('GET', '/projects/1/hooks/2')

        data = { 'test' : 'test' }
        self.service.project(1).hooks().create(data)
        self.expect('POST', '/projects/1/hooks')

        with port.assertRaises(MethodNotSupported):
            self.service.project(1).hooks().update(data)
        with port.assertRaises(MethodNotSupported):
            self.service.project(1).hooks().delete()

        data = { 'test' : 'test' }
        self.service.project(1).hook(2).update(data)
        self.expect('PUT', '/projects/1/hooks/2')

        self.service.project(1).hook(2).delete()
        self.expect('DELETE', '/projects/1/hooks/2')

    def test_merge_requests(self):
        self.service.project(1).merge_requests().get()
        self.expect('GET', '/projects/1/merge_requests')
       
        data = { 'state' : 'closed' }
        self.service.project(1).merge_requests().get(data)
        self.expect('GET', '/projects/1/merge_requests', data)

        self.service.project(1).merge_request(0).get()
        self.expect('GET', '/projects/1/merge_request/0')

        self.service.project(1).merge_request(4).changes()
        self.expect('GET', '/projects/1/merge_request/4/changes')

        data = {'source_branch': "my-first-feature",
                'target_branch': "next",
                'assignee_id': "masterofdesaster",
                'title': "Nice title",
                'description' : "Lets put some content",
                'target_project_id': "forked project id"}

        self.service.project(1).merge_requests().create(data)
        self.expect('POST', '/projects/1/merge_requests', data)

        data = {'source_branch': "my-first-feature",
                'target_branch': "next",
                'assignee_id': "masterofdesaster",
                'title': "Nice title",
                'description' : "Lets put some content",
                'state_event': "closed"}

        self.service.project(1).merge_request(2).update(data)
        self.expect('PUT', '/projects/1/merge_request/2', data)

        self.service.project(1).merge_request(2).accept()
        self.expect('PUT', '/projects/1/merge_request/2/merge')

        data = { 'merge_commit_message' : "really nice featur" }
        self.service.project(1).merge_request(2).accept(data)
        self.expect('PUT', '/projects/1/merge_request/2/merge', data)

        self.service.project(1).merge_request(2).notes().get()
        self.expect('GET', '/projects/1/merge_request/2/notes')

        self.service.project(1).merge_request(2).note(1).get()
        self.expect('GET', '/projects/1/merge_request/2/notes/1')

        self.service.project(1).merge_request(2).comments().get()
        self.expect('GET', '/projects/1/merge_request/2/comments')

        self.service.project(1).merge_request(2).comments().create({ 'note' : 'nice note'})
        self.expect('POST', '/projects/1/merge_request/2/comments', { 'note' : 'nice note'})

        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.project(1).merge_request(2).comments().update({ 'note' : 'a nicer note'}))
        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.project(1).merge_request(2).comments().delete())

    def test_users(self):
        data = { 'test':'test'}

        self.service.users().get(data)
        self.expect('GET', '/users', data, {'PRIVATE-TOKEN': 'my-token'})

        self.service.users().create(data)
        self.expect('POST', '/users', data, {'PRIVATE-TOKEN': 'my-token'})

        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.users().update(data))
        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.users().delete())

        self.service.user(1).get()
        self.expect('GET', '/users/1', {}, {'PRIVATE-TOKEN': 'my-token'})

        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.user(1).create(data))

        self.service.user(1).update(data)
        self.expect('PUT', '/users/1', data, {'PRIVATE-TOKEN': 'my-token'})

        self.service.user(1).delete()
        self.expect('DELETE', '/users/1', {}, {'PRIVATE-TOKEN': 'my-token'})

        self.service.user(1).keys().get()
        self.expect('GET', '/users/1/keys', {}, {'PRIVATE-TOKEN': 'my-token'})

        self.service.user(1).keys().create(data)
        self.expect('POST', '/users/1/keys', data, {'PRIVATE-TOKEN': 'my-token'})

        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.user(1).keys().update(data))
        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.user(1).keys().delete())

        ## not documented in api but who knows does not harm anybody
        self.service.user(1).key(5).get()
        self.expect('GET', '/users/1/keys/5', {}, {'PRIVATE-TOKEN': 'my-token'})

        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.user(1).key(5).create(data))
        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.user(1).key(5).update(data))

        self.service.user(1).key(5).delete()
        self.expect('DELETE', '/users/1/keys/5', {}, {'PRIVATE-TOKEN': 'my-token'})

        # current user
        self.service.user().get()
        self.expect('GET', '/user', {}, {'PRIVATE-TOKEN': 'my-token'})

        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.user().create(data))
        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.user().update(data))
        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.user().delete())

        self.service.user().keys().get()
        self.expect('GET', '/user/keys', {}, {'PRIVATE-TOKEN': 'my-token'})

        self.service.user().keys().create(data)
        self.expect('POST', '/user/keys', data, {'PRIVATE-TOKEN': 'my-token'})

        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.user().keys().update(data))
        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.user().keys().delete())

        self.service.user().key(2).get()
        self.expect('GET', '/user/keys/2', {}, {'PRIVATE-TOKEN': 'my-token'})

        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.user().key(4).create(data))
        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.user().key(4).update(data))

        self.service.user().key(4).delete()
        self.expect('DELETE', '/user/keys/4', {}, {'PRIVATE-TOKEN': 'my-token'})

    def test_issues(self):
        self.service.issues().get()
        self.expect('GET', '/issues')

        self.service.issues().get({'state':"closed", 'labels':'feature,bug'})
        self.expect('GET', '/issues')

        self.service.project(1).issue(2).get()
        self.expect('GET', '/projects/1/issues/2')

        self.service.project(1).issue(2).update({'title':"test title", 'labels':'feature,bug'})
        self.expect('PUT', '/projects/1/issues/2')

        self.service.project(1).issues().get({'title':"test title", 'labels':'feature,bug'})
        self.expect('GET', '/projects/1/issues')

        self.service.project(1).issues().create({'title':"test title", 'labels':'feature,bug'})
        self.expect('POST', '/projects/1/issues')

        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.issues().update({ 'note' : 'a nicer note'}))
        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.issues().create({ 'note' : 'a nicer note'}))
        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.issues().delete())
        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.project(1).issue(1).create({'test':'test'}))
        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.project(1).issue(1).delete())
        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.project(1).issues().update({'test':'test'}))
        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.project(1).issues().delete())

    def test_branches(self):
        data = { 'test' : 'test'}

        self.service.project(1).branches().get()
        self.expect('GET', '/projects/1/repository/branches')

        self.service.project(1).branches().create(data)
        self.expect('POST', '/projects/1/repository/branches', data)

        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.project(1).branches().update(data))
        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.project(1).branches().delete())

        self.service.project(1).branch("branchname").get()
        self.expect('GET', '/projects/1/repository/branches/branchname')

        self.service.project(1).branch("branchname").protect()
        self.expect('PUT', '/projects/1/repository/branches/branchname/protect')

        self.service.project(1).branch("branchname").unprotect()
        self.expect('PUT', '/projects/1/repository/branches/branchname/unprotect')

        self.service.project(1).branch("branchname").delete()
        self.expect('DELETE', '/projects/1/repository/branches/branchname')

        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.project(1).branch(2).update(data))
        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.project(1).branch(2).create(data))

    def test_commits(self):
        data = { 'test' : 'test'}

        self.service.project(1).commits().get()
        self.expect('GET', '/projects/1/repository/commits')

        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.project(1).commits().create(data))
        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.project(1).commits().update(data))
        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.project(1).commits().delete())

        self.service.project(1).commit("sha").get()
        self.expect('GET', '/projects/1/repository/commits/sha')

        self.service.project(1).commit("sha2").get_diff()
        self.expect('GET', '/projects/1/repository/commits/sha2/diff')

        self.service.project(1).commit("shaadfaf").get_comments()
        self.expect('GET', '/projects/1/repository/commits/shaadfaf/comments')

        self.service.project(1).commit("shaf3434fasdf").post_comment(data)
        self.expect('POST', '/projects/1/repository/commits/shaf3434fasdf/comments', data)

        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.project(1).commit("sha").create(data))
        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.project(1).commit("sha").update(data))
        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.project(1).commit("sha").delete())

    def test_keys(self):
        data = { 'test' : 'test'}

        self.service.project(1).keys().get()
        self.expect('GET', '/projects/1/keys')

        self.service.project(1).keys().create(data)
        self.expect('POST', '/projects/1/keys', data)

        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.project(1).keys().update(data))
        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.project(1).keys().delete())

        self.service.project(1).key(3).get()
        self.expect('GET', '/projects/1/keys/3')

        self.service.project(1).key(3).delete()
        self.expect('DELETE', '/projects/1/keys/3')

        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.project(1).key(2).create(data))
        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.project(1).key(3).update(data))

    def test_groups(self):
        data = { 'test' : 'test'}

        self.service.groups().get()
        self.expect('GET', '/groups')

        self.service.groups().search("test")
        self.expect('GET', '/groups', { "search":"test"} )

        self.service.groups().create(data)
        self.expect('POST', '/groups', data)

        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.groups().update(data))
        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.groups().delete())

        self.service.group(1).get()
        self.expect('GET', '/groups/1')

        self.service.group(1).delete()
        self.expect('DELETE', '/groups/1')

        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.group(1).create(data))
        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.group(1).update(data))

        # admin only
        self.service.group(1).transfer_project(3)
        self.expect('POST', '/groups/1/projects/3')

        self.service.group(1).members().get()
        self.expect('GET', '/groups/1/members')

        self.service.group(1).members().create(data)
        self.expect('POST', '/groups/1/members', data)

        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.group(1).members().update(data))
        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.group(1).members().delete())

        self.service.group(1).member(3).update(data)
        self.expect('PUT', '/groups/1/members/3', data)

        self.service.group(1).member(3).delete()
        self.expect('DELETE', '/groups/1/members/3')

        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.group(1).member(4).get())
        with port.assertRaises(MethodNotSupported):
            self.assertRaises(self.service.group(1).member(3).create(data))
