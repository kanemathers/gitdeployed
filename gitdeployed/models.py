import logging

import git

from sqlalchemy import (
    Column,
    Integer,
    Text,
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
