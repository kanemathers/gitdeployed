import tempfile
import os.path
import shutil

from pyramid.view import (
    view_config,
    view_defaults,
)

from pyramid.renderers import render_to_response
from pyramid.httpexceptions import (
    HTTPNoContent,
    HTTPBadRequest,
    HTTPNotFound,
    HTTPFound,
)

from pyramid.security import (
    remember,
    forget,
)

from mako.exceptions import TopLevelLookupException

from .models import (
    DBSession,
    Users,
    Repos,
)

@view_config(route_name='home', renderer='index.mako')
def home(request):
    return {}

@view_config(route_name='partial')
def partial(request):
    """ Renders and returns the Mako template named ``partial``. """

    partial = request.matchdict['partial']
    path    = 'gitdeployed:templates/{0}.mako'.format(partial)

    try:
        return render_to_response(path, {}, request=request)
    except TopLevelLookupException:
        return HTTPNotFound()

class UserViews(object):

    def __init__(self, request):
        self.request = request

    @view_config(route_name='user.login', request_method='POST',
                 renderer='json')
    def login(self):
        """ Authenticate the user. """

        email    = self.request.json_body.get('email')
        password = self.request.json_body.get('password')

        user = Users.by_email(email)

        if not user or not user.check_password(password):
            return HTTPBadRequest(body='Invalid username or password')

        self.request.response.headerlist += remember(self.request, user.id)

        return {'user': user}

    @view_config(route_name='user.logout', request_method='GET')
    def logout(self):
        """ Destroy the users session. """

        return HTTPFound(location=self.request.route_path('home'),
                         headers=forget(self.request))

@view_defaults(permission='view')
class RepoViews(object):

    def __init__(self, request):
        self.request = request

    @view_config(route_name='repos', request_method='GET', renderer='json')
    def all(self):
        """ Returns a list of all the repositories. """

        return Repos.all()

    @view_config(route_name='repos.get', request_method='GET', renderer='json')
    def get(self):
        """ Returns the config shit for the repository. """

        return Repos.by_id(self.request.matchdict['id'])

    @view_config(route_name='repos', request_method='POST')
    def new(self):
        """ Create and save a new git repository. """

        def make_path():
            """ Creates a new directory and returns the path.

            The directory will be created at the root folder specified in the
            setting ``repos.root_path``.
            """

            settings  = self.request.registry.settings
            root_path = settings['repos.root_path']

            return tempfile.mkdtemp(prefix='', suffix='.git', dir=root_path)

        try:
            path     = self.request.json_body.get('path') or make_path()
            upstream = self.request.json_body['upstream']
        except KeyError:
            return HTTPBadRequest(body='Invalid path or upstream')

        repo = Repos(path, upstream)
        repo.save(flush=True)
        repo.clone()

        return HTTPFound(location=self.request.route_path('repos.get',
                                                          id=repo.id))

    @view_config(route_name='repos.sync', request_method='POST')
    def sync(self):
        """ Syncs the local repository with upstream.

        ``git pull origin master``, esentially.
        """

        try:
            repo = Repos.by_id(self.request.matchdict['id'])
        except KeyError:
            return HTTPBadRequest()

        repo.pull()

        return HTTPNoContent()

    @view_config(route_name='repos.get', request_method='DELETE')
    def delete(self):
        """ Delete the repository with the specified ``id``.

        If ``hdd`` is True, the repository itself will also be removed.
        This may fail due to permissions errors, however.
        """

        try:
            repo = Repos.by_id(self.request.matchdict['id'])
        except KeyError:
            return HTTPNotFound()

        repo.delete()

        if self.request.GET.get('hdd', False):
            shutil.rmtree(repo.path)

        return HTTPNoContent()
