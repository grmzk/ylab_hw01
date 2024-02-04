from database import Base


class ExtendedBase(Base):
    __abstract__ = True

    def update(self, **kwargs):
        """Update fields values."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in
                self.__table__.columns}
