from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import (
    HTTPOk,
    HTTPBadRequest,
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

@view_config(route_name='repos', request_method='GET', renderer='json')
def repo_list(request):
    """ Returns a list of all the repositories. """

    return Repos.all()

@view_config(route_name='repos', request_method='POST', renderer='json')
def repo_create(request):
    """ Create and save a new git repository. """

    try:
        name        = request.json_body['name']
        description = request.json_body['description']
        path        = request.json_body['path']
        upstream    = request.json_body['upstream']
    except (KeyError, ValueError):
        return HTTPBadRequest()

    repo = Repos(name, description, path, upstream)
    repo.save()

    return HTTPOk()
