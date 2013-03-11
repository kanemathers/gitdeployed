import datetime
import string
import random

from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.renderers import JSON

from sqlalchemy import engine_from_config

from webassets import Bundle

from .models import (
    DBSession,
    Base,
)

from .factories import ReposFactory

def generate_secret():
    """ Returns a randomly generated string for use in signing/hashing the
    cookies.
    """

    return ''.join(random.choice(string.letters + string.digits)
                   for i in xrange(20))

def patch_json_renderer():
    """ Returns a patched JSON renderer capable of serializing custom
    objects.
    """

    def datetime_adapter(obj, request):
        return int(obj.strftime('%s'))

    renderer = JSON()
    renderer.add_adapter(datetime.datetime, datetime_adapter)

    return renderer

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application. """

    authn_policy = AuthTktAuthenticationPolicy(settings.get('auth.secret',
                                                            generate_secret()))
    authz_policy = ACLAuthorizationPolicy()

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config = Configurator(settings=settings)

    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_renderer('json', patch_json_renderer())

    config.add_route('home', '/')
    config.add_route('partial', '/partials/{partial}.html')

    config.add_route('user.login', '/login')
    config.add_route('user.logout', '/logout')

    config.add_route('repos', '/repos', factory=ReposFactory)
    config.add_route('repos.get', '/repos/{id}', factory=ReposFactory)
    config.add_route('repos.sync', '/repos/{id}/sync', factory=ReposFactory)

    bundle_js   = Bundle('js/*.js',
                         filters='rjsmin', output='js/app.min.js', debug=False)
    bundle_less = Bundle('css/app.less',
                         filters='less', output='css/app.min.css', debug=False)

    config.add_webasset('js', bundle_js)
    config.add_webasset('less', bundle_less)

    config.scan()

    return config.make_wsgi_app()
