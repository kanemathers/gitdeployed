import logging
import shlex
import datetime

import git
import bcrypt

from sqlalchemy import (
    Column,
    Integer,
    Text,
    Unicode,
    DateTime,
    BINARY,
)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)

from zope.sqlalchemy import ZopeTransactionExtension

log = logging.getLogger(__name__)

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base      = declarative_base()

class BaseMixins(object):
    """ Generic mixins for SQLAlchemy base classes. """

    @classmethod
    def all(cls):
        """ Returns all objects from the database. """

        return DBSession.query(cls).all()

    @classmethod
    def by_id(cls, id):
        """ Returns the object with the given ``id``. """

        return DBSession.query(cls).filter(cls.id == id).first()

    def save(self, flush=False):
        """ Creates and saves the object into the database.

        If ``flush`` is ``True``, the write will be immediately commited to
        the database.
        """

        DBSession.add(self)

        if flush:
            DBSession.flush()

    def delete(self):
        """ Deletes the object from the database. """

        DBSession.delete(self)

class Users(Base, BaseMixins):

    __tablename__ = 'users'

    id       = Column(Integer, primary_key=True)
    email    = Column(Unicode(255), unique=True, index=True)
    password = Column(BINARY(60))
    created  = Column(DateTime, default=datetime.datetime.now)

    def __init__(self, email, password):
        self.email    = email
        self.password = self.hash_password(password)

    def __json__(self, request):
        return {
            'id':      self.id,
            'email':   self.email,
            'created': self.created,
        }

    @classmethod
    def by_email(cls, email):
        """ Returns the user object with the specified ``email``. """

        return DBSession.query(cls).filter(cls.email == email).one()

    def check_password(self, password):
        """ Checks if the supplied ``password`` matches the users saved
        password.
        """

        return bcrypt.hashpw(password, self.password) == self.password

    @staticmethod
    def hash_password(password):
        """ Hashes the ``password`` and returns the string. """

        return bcrypt.hashpw(password, bcrypt.gensalt())

class Repos(Base, BaseMixins):

    __tablename__ = 'repos'

    id       = Column(Integer, primary_key=True)
    path     = Column(Integer)
    upstream = Column(Integer)

    def __init__(self, path, upstream):
        self.path     = path
        self.upstream = upstream

    def __json__(self, request):
        return {
            'id':       self.id,
            'path':     self.path,
            'upstream': self.upstream,
            #'log':      self.log(),
        }

    def clone(self):
        """ ``git clone`` the ``upstream`` repository into the ``path``. """

        log.info('Cloning "{0}" into "{1}"'.format(self.upstream, self.path))

        return git.Repo.clone_from(self.upstream, self.path)

    def pull(self):
        """ ``git pull`` from the upstream repository. """

        log.info('Pulling "{0}" into "{1}"'.format(self.upstream, self.path))

        repo   = git.Repo(self.path)
        origin = repo.remotes.origin

        return origin.pull()

    def log(self):
        """ Returns the recent commit log. """

        g   = git.Git(self.path)
        cmd = '--pretty=format:"%h %ad | %s%d [%an]" --graph --date=short'
        cmd = shlex.split(cmd)

        return g.log(*cmd).split('\n')
