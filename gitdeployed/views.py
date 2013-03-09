import tempfile
import os.path

from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import (
    HTTPNoContent,
    HTTPBadRequest,
    HTTPNotFound,
    HTTPFound,
)

from mako.exceptions import TopLevelLookupException

from .models import (
    DBSession,
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

    @view_config(route_name='repos', request_method='POST', renderer='json')
    def new(self):
        """ Create and save a new git repository. """

        def make_path():
            """ Creates a new directory and returns the path.

            The directory will be created at the root folder specified in the
            setting ``repos.root_path``.
            """

            settings  = self.request.registry.settings
            root_path = settings['repos.root_path']

            return tempfile.mkdtemp(dir=root_path)

        try:
            path     = self.request.json_body['path']
            upstream = self.request.json_body['upstream']
        except (KeyError, ValueError):
            return HTTPBadRequest()

        repo = Repos(path or make_path(), upstream)

        repo.save(flush=True)
        repo.clone()

        return HTTPFound(location=self.request.route_path('repos.get',
                                                          id=repo.id))

    @view_config(route_name='repos.sync', request_method='POST',
                 renderer='json')
    def sync(request):
        """ Syncs the local repository with upstream.

        ``git pull origin master``, esentially.
        """

        try:
            repo = Repos.by_id(self.request.matchdict['id'])
        except KeyError:
            return HTTPBadRequest()

        repo.pull()

        return HTTPNoContent()
