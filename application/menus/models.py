import uuid

from sqlalchemy import UUID, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from database import Base


class ExtendedBase(Base):
    __abstract__ = True

    def update(self, **kwargs):
        """Update fields values."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class Menu(ExtendedBase):
    __tablename__ = "menus"
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    submenus = relationship("Submenu", back_populates="menu",
                            cascade="all, delete-orphan")


class Submenu(ExtendedBase):
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


class Dish(ExtendedBase):
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
