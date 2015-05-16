import json

from libsaas import http
from libsaas.filters import auth
from libsaas.services import base

from . import resource
from . import projects
from . import users
from . import issues
from . import groups

class Gitlab(base.Resource):
    """
    """
    def __init__(self, host, token_or_username, oauth_token=None, password=None):
        """
        Create a GitLab serivce.

        :var host: Url of GitLab server
        :vartype host: str

        :var token_or_username: Either an token, or the username if
          you want to use Basic authentication.
        :vartype token_or_username: str

        :var oauth_token: OAuth 2.0 token
        :vartype oauth_token: str

        :var password: Only used with the Basic authentication, leave this as
            `None` when using OAuth.
        :vartype password: str
        """
        self.apiroot    = host + "/api/v3"

        if password is None:
          if oauth_token:
            self.oauth_token = oauth_token
            self.add_filter(self.add_authorization)
          else:   
            self.token   = token_or_username
            self.add_filter(self.add_privatetoken_authorization)
        else:
            self.add_filter(auth.BasicAuth(token_or_username, password))

    def add_authorization(self, request):
        request.headers['Authorization'] = 'Bearer {0}'.format(self.oauth_token)

    def add_privatetoken_authorization(self, request):
        request.headers['PRIVATE-TOKEN'] = self.token

    def get_url(self):
        return self.apiroot

    @base.resource(users.User, users.CurrentUser)
    def user(self, user_id=None):
        """
        Return the resource corresponding to a single user. If `user_id` is `None`
        the returned resource is the currently authenticated user, otherwise it
        is the user with the given user_id.
        """
        if user_id:
            return users.User(self, user_id)
        return users.CurrentUser(self)

    @base.resource(users.Users)
    def users(self):
        """
        Return the resource corresponding to all users. 
        """
        return users.Users(self)

    @base.resource(projects.Project)
    def project(self, project_id):
        """
        Return the resource corresponding to a single project.
        """
        return projects.Project(self, project_id)

    @base.resource(projects.Projects)
    def projects(self):
        """
        Return the resource corresponding to all the projects.
        """
        return projects.Projects(self)

    @base.resource(issues.Issues)
    def issues(self):
        """
        Return the resource corresponding to all the projects.
        """
        return issues.Issues(self)

    @base.resource(groups.Group)
    def group(self, group_id):
        """
        Return the resource corresponding to all the groups.
        """
        return groups.Group(self, group_id)

    @base.resource(groups.Groups)
    def groups(self):
        """
        Return the resource corresponding to all the groups.
        """
        return groups.Groups(self)

    @base.resource(resource.Session)
    def session(self):
        """
        Return the resource corresponding to a session
        """
        return resource.Session(self)

    @base.resource(resource.Hook)
    def hook(self, hook_id):
        """
        Return the resource corresponding to a hook
        """
        return resource.Hook(self, hook_id)

    @base.resource(resource.Hooks)
    def hooks(self):
        """
        Return the resource corresponding to all hooks
        """
        return resource.Hooks(self)

Gitlab = Gitlab
