from pydantic import BaseModel, ConfigDict, Field, field_serializer
from pydantic.types import UUID4


class MenuReadSchema(BaseModel):
    model_config = ConfigDict(extra='allow')

    id: UUID4 | None
    title: str
    description: str
    submenus: list = Field(serialization_alias="submenus_count")
    dishes_count: int = 0

    @field_serializer("submenus")
    def get_submenus_count(self, submenus: list) -> int:
        return len(submenus)

    @field_serializer("dishes_count")
    def get_dishes_count(self, arg) -> int:
        dishes_count = 0
        for submenu in self.submenus:
            dishes_count += len(submenu.dishes)
        return dishes_count


class MenuWriteSchema(BaseModel):
    title: str = Field(max_length=250)
    description: str = Field(max_length=250)


class SubmenuReadSchema(BaseModel):
    id: UUID4 | None
    title: str
    description: str
    dishes: list = Field(serialization_alias="dishes_count")

    @field_serializer("dishes")
    def get_dishes_count(self, dishes: list) -> int:
        return len(dishes)


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
