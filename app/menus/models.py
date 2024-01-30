import uuid

from sqlalchemy import UUID, Column, ForeignKey, String, func
from sqlalchemy.orm import Query, relationship

from database import Base, Session
from menus.schemas import DishReadSchema, MenuReadSchema, SubmenuReadSchema
from menus.utils.extendedbase import ExtendedBase


class Menu(ExtendedBase, Base):
    __schema__ = MenuReadSchema

    __tablename__ = "menus"
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    submenus = relationship("Submenu", back_populates="menu",
                            cascade="all, delete-orphan")

    @staticmethod
    def get_query(session: Session) -> Query:
        """Return query to get Menu rows from database."""
        return (session.query(
            Menu,
            func.count(func.distinct(Submenu.id)).label("submenus_count"),
            func.count(func.distinct(Dish.id)).label("dishes_count"))
            .outerjoin(Submenu, Submenu.menu_id == Menu.id)
            .outerjoin(Dish, Dish.submenu_id == Submenu.id)
            .group_by(Menu.id))


class Submenu(ExtendedBase, Base):
    __schema__ = SubmenuReadSchema

    __tablename__ = "submenus"
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    menu_id = Column(UUID, ForeignKey("menus.id"))
    menu = relationship("Menu", back_populates="submenus")
    dishes = relationship("Dish", back_populates="submenu",
                          cascade="all, delete-orphan")

    def check_parent_menu(self, menu_id: UUID) -> bool:
        """Check parent by his UUID."""
        return self.menu_id == menu_id

    @classmethod
    def get_schema_objects_by_menu(cls, session: Session,
                                   menu_id: UUID) -> list:
        query = cls.get_query(session).filter(cls.menu_id == menu_id)
        return cls.get_schema_objects(session, query)

    @staticmethod
    def get_query(session: Session) -> Query:
        """Return query to get Submenu rows from database."""
        return (session.query(
            Submenu,
            func.count(func.distinct(Dish.id)).label("dishes_count"))
            .outerjoin(Dish, Dish.submenu_id == Submenu.id)
            .group_by(Submenu.id))


class Dish(ExtendedBase, Base):
    __schema__ = DishReadSchema

    __tablename__ = "dishes"
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(String, nullable=False)
    submenu_id = Column(UUID, ForeignKey("submenus.id"))
    submenu = relationship("Submenu", back_populates="dishes")

    def check_parent_submenu(self, submenu_id: UUID) -> bool:
        """Check parent by his UUID."""
        return self.submenu_id == submenu_id

    @classmethod
    def get_schema_objects_by_submenu(cls, session: Session,
                                      submenu_id: UUID) -> list:
        query = cls.get_query(session).filter(cls.submenu_id == submenu_id)
        return cls.get_schema_objects(session, query)

    @staticmethod
    def get_query(session: Session) -> Query:
        """Return query to get Dish rows from database."""
        return session.query(Dish)
