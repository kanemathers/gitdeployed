import os
import sys
import transaction
import argparse
import getpass

from sqlalchemy import engine_from_config

from paste.deploy import loadapp
from waitress import serve

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from ..models import (
    DBSession,
    Base,
    Users,
)

def init_db(engine):
    """ Initialize the database. """

    Base.metadata.create_all(engine)

def create_user(email):
    """ Creates a new user with the ``email`` and ``password``. """

    password = getpass.getpass('Password for {0}: '.format(email))

    with transaction.manager:
        Users(email, password).save()

def main(argv=sys.argv):
    desc   = ('Centralised interface to manage your servers incoming git POST '
              'service hooks.')
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('-i', '--init-db', action='store_true',
                        default=False, help='initialize the database')
    parser.add_argument('-e', '--email', nargs=1,
                        help='setup a new user account')
    parser.add_argument('config', help='path to the config file')

    args = parser.parse_args()

    config_uri = args.config
    setup_logging(config_uri)

    settings = get_appsettings(config_uri)
    engine   = engine_from_config(settings, 'sqlalchemy.')

    DBSession.configure(bind=engine)

    if args.init_db:
        init_db(engine)

    if args.email:
        create_user(args.email[0])

    app = loadapp('config:{0}'.format(config_uri), relative_to='.')
    serve(app, host='0.0.0.0', port=6543)
