from pydantic import BaseModel, Field
from pydantic.types import UUID4


class MenuReadSchema(BaseModel):
    id: UUID4 | None
    title: str
    description: str
    submenus_count: int = 0
    dishes_count: int = 0


class MenuWriteSchema(BaseModel):
    title: str = Field(max_length=250)
    description: str = Field(max_length=250)


class SubmenuReadSchema(BaseModel):
    id: UUID4 | None
    title: str
    description: str
    dishes_count: int = 0


class SubmenuWriteSchema(BaseModel):
    title: str = Field(max_length=250)
    description: str = Field(max_length=250)


class DishReadSchema(BaseModel):
    id: UUID4 | None
    title: str
    description: str
    price: str


class DishWriteSchema(BaseModel):
    title: str = Field(max_length=250)
    description: str = Field(max_length=250)
    price: str = Field(max_length=250, pattern=r"^\d+\.\d{2}$")
