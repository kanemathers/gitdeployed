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

    id          = Column(Integer, primary_key=True)
    name        = Column(Text, unique=True)
    description = Column(Integer)
    path        = Column(Integer)
    upstream    = Column(Integer)

    def __init__(self, name, description, path, upstream):
        self.name        = name
        self.description = name
        self.path        = name
        self.upstream    = name
