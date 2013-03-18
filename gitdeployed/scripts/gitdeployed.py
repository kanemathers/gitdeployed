import os
import sys
import transaction
import argparse
import getpass

from sqlalchemy import engine_from_config

from pyramid.scripts import pserve

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

def create_user(username):
    """ Creates a new user with the ``username``. You will be prompted to
    enter a password via stdin.
    """

    password = getpass.getpass('Password for {0}: '.format(username))
    confirm  = getpass.getpass('Again: ')

    if password != confirm:
        print >> sys.stderr, "Passwords don't match"

        sys.exit(1)

    with transaction.manager:
        Users(username, password).save()

def main(argv=sys.argv):
    desc   = ('gitdeployed allows you to easily setup the end points for all '
              'your POST service hooks.')
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('-i', '--init-db', action='store_true',
                        default=False, help='initialize the database')
    parser.add_argument('-n', '--no-serve', action='store_true',
                        default=False, help="don't enable the web server")
    parser.add_argument('-u', '--username', nargs=1,
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

    if args.username:
        create_user(args.username[0])

    if not args.no_serve:
        pserve.PServeCommand([None, config_uri]).run()
