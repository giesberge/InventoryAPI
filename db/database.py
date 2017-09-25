# -*- coding: utf-8 -*-
"""Database module, including the SQLAlchemy database object and DB-related utilities."""
from .compat import basestring
from apistar.backends.sqlalchemy_backend import Session
from apistar import Response
import sqlalchemy.types as db
import sqlalchemy.sql.functions as func
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from .meta import Base
import hashlib


class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, session: Session, commit=True):
        """Save the record."""
        session.add(self)
        if commit:
            session.commit()
        session.flush()
        return self

    def delete(self, session:Session, commit=True):
        """Remove the record from the database."""
        session.delete(self)
        return commit and session.commit()


class Model(CRUDMixin, Base):
    """Base model class that includes CRUD convenience methods."""
    __abstract__ = True
    _created = Column(db.DateTime, default=func.now())
    _updated = Column(db.DateTime, default=func.now(), onupdate=func.now())
    _etag = Column(db.String(40))

    def __init__(self, *args, **kwargs):
        h = hashlib.sha1()
        self._etag = h.hexdigest()
        super(Model, self).__init__(*args, **kwargs)


# From Mike Bayer's "Building the app" talk
# https://speakerdeck.com/zzzeek/building-the-app
class SurrogatePK(object):
    """A mixin that adds a surrogate integer 'primary key' column named ``id`` to any declarative-mapped class."""

    __table_args__ = {'extend_existing': True}

    _id = Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        if any(
                (isinstance(record_id, basestring) and record_id.isdigit(),
                 isinstance(record_id, (int, float))),
        ):
            return cls.query.get(int(record_id))
        return None

    @classmethod
    def api_delete(cls, session:Session, record_id: int):
        res = cls.get_by_id(record_id)
        if res:
            success = res.delete(session)
            if success:
                return Response(status=204)
            else:
                return Response(status=500)
        else:
            return Response(status=404)

    @classmethod
    def api_edit(cls, session:Session, record_id: int, *args, **kwargs):
        res = cls.get_by_id(record_id)
        if res:
            success = cls.update(*args, **kwargs)

        return Response(status=501)


def reference_col(tablename, nullable=False, pk_name='_id', **kwargs):
    """Column that adds primary key foreign key reference.

    Usage: ::

        category_id = reference_col('category')
        category = relationship('Category', backref='categories')
    """
    return Column(
        ForeignKey('{0}.{1}'.format(tablename, pk_name)),
        nullable=nullable, **kwargs)