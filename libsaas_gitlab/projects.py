from libsaas import http, parsers
from libsaas.services import base

from . import resource
from . import merge_requests
from . import issues
from . import branches
from . import commits
from . import keys

class ProjectsBase(resource.GitlabResource):
    path = 'projects'

class Projects(ProjectsBase):

    @base.apimethod
    def get(self, data=None):
        """
        Fetch projects the user has access to.

        :var owned_or_all: Is owner of the project
        """
        url    = self.get_url()
        if data and 'owned_or_all' in data:
            url = [ url, url + "/owned"][ "owned" == data['owned_or_all']]
            url = [ url, url + "/all"][ "all" == data['owned_or_all']]
            del data['owned_or_all']

        params = data
        return http.Request('GET', url, params), parsers.parse_json

    @base.apimethod
    def create_for_user(self, user_id, data = None):
        """
        Create project for user - admin only
        """
        url = '{0}/user/{1}'.format(self.get_url(), user_id)

        return http.Request('POST', url, data), parsers.parse_json

    @base.apimethod
    def search(self, query, data = None):
        """
        Search for projects by name
        """
        url = '{0}/search/{1}'.format(self.get_url(), query)

        return http.Request('GET', url, data), parsers.parse_json

class Project(ProjectsBase):

    @base.apimethod
    def events(self):
        """
        Fetch events
        """
        url = '{0}/events'.format(self.get_url())

        return http.Request('GET', url), parsers.parse_json

    @base.apimethod
    def fork(self):
        """
        Fork project
        """
        url = '{0}/fork/{1}'.format(self.parent.get_url() + "/" + self.path, self.object_id)

        return http.Request('POST', url), parsers.parse_json

    @base.apimethod
    def add_fork_relation(self, forked_from_id):
        """
        Add relation from forked id
        """
        url = '{0}/fork/{1}'.format(self.get_url(), forked_from_id)

        return http.Request('POST', url), parsers.parse_json

    @base.apimethod
    def delete_fork_relation(self):
        """
        Add relation from forked id
        """
        url = '{0}/fork'.format(self.get_url())

        return http.Request('DELETE', url), parsers.parse_json

    @base.resource(merge_requests.MergeRequest)
    def merge_request(self, merge_request_id):
        """
        Return a resource corresponding to a single merge request for this project.
        """
        return merge_requests.MergeRequest(self, merge_request_id)

    @base.resource(merge_requests.MergeRequests)
    def merge_requests(self):
        """
        Return a resource corresponding to all merge requests for this project.
        """
        return merge_requests.MergeRequests(self)

    @base.resource(issues.ProjectIssue)
    def issue(self, issue_id):
        """
        Return a resource corresponding to a single issue for this project.
        """
        return issues.ProjectIssue(self, issue_id)

    @base.resource(issues.ProjectIssues)
    def issues(self):
        """
        Return a resource corresponding to a all issues for this project.
        """
        return issues.ProjectIssues(self)

    @base.resource(resource.MembersBase)
    def members(self):
        """
        Get members
        """
        return resource.MembersBase(self)

    @base.resource(resource.MembersBase)
    def member(self, user_id):
        """
        Get team member by id
        """
        return resource.MembersBase(self, user_id)

    @base.resource(resource.HooksBase)
    def hooks(self):
        """
        Get hooks
        """
        return resource.HooksBase(self)

    @base.resource(resource.HooksBase)
    def hook(self, hook_id):
        """
        Get a hook
        """
        return resource.HooksBase(self, hook_id)

    @base.resource(branches.Branch)
    def branch(self, branch):
        """
        Get a branch
        """
        return branches.Branch(self, branch)

    @base.resource(branches.BranchesBase)
    def branches(self):
        """
        Get branches
        """
        return branches.BranchesBase(self)

    @base.resource(commits.Commit)
    def commit(self, sha):
        """
        Get a commit
        """
        return commits.Commit(self, sha)

    @base.resource(commits.CommitsBase)
    def commits(self):
        """
        Get commmits
        """
        return commits.CommitsBase(self)

    @base.resource(keys.Key)
    def key(self, key_id):
        """
        Get a key
        """
        return keys.Key(self, key_id)

    @base.resource(keys.Keys)
    def keys(self):
        """
        Get keys
        """
        return keys.Keys(self)

    @base.resource(resource.LabelsBase)
    def labels(self):
        """
        Get labels
        """
        return resource.LabelsBase(self)

    @base.resource(resource.Milestone)
    def milestone(self, milestone_id):
        """
        Get milestone
        """
        return resource.Milestone(self, milestone_id)

    @base.resource(resource.Milestones)
    def milestones(self):
        """
        Get milestones
        """
        return resource.Milestones(self)

    @base.resource(resource.Snippet)
    def snippet(self, snippet_id):
        """
        Get snippet
        """
        return resource.Snippet(self, snippet_id)

    @base.resource(resource.Snippets)
    def snippets(self):
        """
        Get snippets
        """
        return resource.Snippets(self)

    @base.resource(resource.RepositoryBase)
    def repository(self):
        """
        Get repository
        """
        return resource.RepositoryBase(self)

    @base.resource(resource.ServicesBase)
    def service(self, name):
        """
        Get service resource
        """
        return resource.ServicesBase(self, name)
