import uuid

from sqlalchemy import UUID, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from database import Base
from menus.utils.extended_base import ExtendedBase


class Menu(ExtendedBase, Base):
    __tablename__ = "menus"
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    submenus = relationship("Submenu", back_populates="menu",
                            cascade="all, delete-orphan")


class Submenu(ExtendedBase, Base):
    __tablename__ = "submenus"
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    menu_id = Column(UUID, ForeignKey("menus.id"))
    menu = relationship("Menu", back_populates="submenus")
    dishes = relationship("Dish", back_populates="submenu",
                          cascade="all, delete-orphan")


class Dish(ExtendedBase, Base):
    __tablename__ = "dishes"
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(String, nullable=False)
    submenu_id = Column(UUID, ForeignKey("submenus.id"))
    submenu = relationship("Submenu", back_populates="dishes")
