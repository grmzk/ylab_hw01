from abc import abstractmethod

from sqlalchemy import UUID, Row
from sqlalchemy.orm import Query

from database import Base, Session
from menus.utils.jsonresponse404 import JSONResponse404


class ExtendedBase(Base):
    __abstract__ = True

    __schema__ = None  # Child of pydantic.BaseModel class

    def update(self, **kwargs):
        """Update fields values."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in
                self.__table__.columns}

    @staticmethod
    @abstractmethod
    def get_query(session: Session) -> Query:
        """Return query for get object from database.
        Query result format must be:
        (<ExtendedBase object>, <additional field>, <additional field>, ...).
        Additional fields are optional."""
        pass

    @classmethod
    def create_from_row(cls, row: Row):
        attrs = dict()
        for key, value in row._asdict().items():
            if hasattr(cls, key):
                attrs[key] = value
        return cls(**attrs)

    @classmethod
    def convert_row_to_schema_obj(cls, row: Row):
        if issubclass(row.__class__, ExtendedBase):
            return cls.__schema__.model_construct(**row.as_dict())
        schema_attrs = dict()
        for key, value in row._asdict().items():
            if issubclass(value.__class__, ExtendedBase):
                schema_attrs.update(value.as_dict())
                continue
            schema_attrs[key] = value
        return cls.__schema__.model_construct(**schema_attrs)

    @classmethod
    def get_schema_objects(cls, session: Session, query: Query = None) -> list:
        """Return a list of BaseModel objects from the database."""
        if not query:
            query = cls.get_query(session)
        schema_objects = list()
        for row in query.all():
            schema_objects.append(cls.convert_row_to_schema_obj(row))
        return schema_objects

    @classmethod
    def get_row_or_404(cls, session: Session, item_id: UUID):
        """Return a Row object from the database
        or return JSONResponse with code 404."""
        row = cls.get_query(session).filter(cls.id == item_id).first()
        return (row
                or JSONResponse404(
                    content={"detail": f"{cls.__name__.lower()} not found"}))

    @classmethod
    def get_schema_obj_or_404(cls, session: Session, item_id: UUID):
        """Return a BaseModel object from the database
        or return JSONResponse with code 404."""
        row = cls.get_row_or_404(session, item_id)
        if row.__class__ is JSONResponse404:
            return row  # response with http code 404
        return cls.convert_row_to_schema_obj(row)

    @classmethod
    def get_or_404(cls, session: Session, item_id: UUID):
        """Return a class object from the database
        or return JSONResponse with code 404."""
        row = cls.get_row_or_404(session, item_id)
        if row.__class__ is JSONResponse404:
            return row  # response with http code 404
        if row.__class__ is Row:
            return row[0]
        return row
