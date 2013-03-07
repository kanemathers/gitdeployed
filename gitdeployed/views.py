from pyramid.view import view_config
from pyramid.httpexceptions import HTTPBadRequest

from .models import (
    DBSession,
    Repos,
)

@view_config(route_name='home', renderer='index.mako')
def home(request):
    return {}

@view_config(route_name='repos.list', renderer='json')
def repo_list(request):
    """ Returns a list of all the repositories. """

    return {'repositories': Repos.all()}

@view_config(route_name='repos.new', request_method='POST', renderer='json')
def repo_create(request):
    """ Create and save a new git repository. """

    try:
        name        = request.json_body['name']
        description = request.json_body['description']
        path        = request.json_body['path']
        upstream    = request.json_body['upstream']
    except KeyError:
        return HTTPBadRequest()

    repo = Repos(name, description, path)
    repo.save()
