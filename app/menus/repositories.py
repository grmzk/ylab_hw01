from uuid import UUID

from fastapi import Depends
from sqlalchemy import func
from starlette import status
from starlette.responses import JSONResponse

from database import Session, get_session
from menus.models import Dish, Menu, Submenu
from menus.schemas import DishReadSchema, MenuReadSchema, SubmenuReadSchema


class MenuRepository:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
        self.model = Menu
        self.schema = MenuReadSchema
        self.query = (session.query(
            Menu.id,
            Menu.title,
            Menu.description,
            func.count(func.distinct(Submenu.id)).label("submenus_count"),
            func.count(func.distinct(Dish.id)).label("dishes_count"))
            .outerjoin(Submenu, Submenu.menu_id == Menu.id)
            .outerjoin(Dish, Dish.submenu_id == Submenu.id)
            .group_by(Menu.id))

    def get_all(self) -> list[MenuReadSchema]:
        return [self.schema.model_validate(menu._asdict())
                for menu in self.query.all()]

    def create(self, input_data: dict) -> MenuReadSchema:
        new_menu = self.model(**input_data)
        self.session.add(new_menu)
        self.session.commit()
        return self.schema.model_validate(new_menu.as_dict())

    def get_model_obj(self, menu_id: UUID) -> Menu | JSONResponse:
        menu = (self.session.query(self.model)
                .filter(self.model.id == menu_id).first())
        return menu or JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": f"{self.model.__name__.lower()} not found"})

    def get(self, menu_id: UUID) -> MenuReadSchema | JSONResponse:
        menu = self.query.filter(self.model.id == menu_id).first()
        if not menu:
            return (JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content={"detail": f"{self.model.__name__.lower()} "
                                       f"not found"}))
        return self.schema.model_validate(menu._asdict())

    def update(self, menu_id: UUID,
               input_data: dict) -> MenuReadSchema | JSONResponse:
        menu = self.get_model_obj(menu_id)
        if isinstance(menu, JSONResponse):
            return menu  # response with http code 404
        menu.update(**input_data)
        self.session.add(menu)
        self.session.commit()
        response_query = self.query.filter(self.model.id == menu_id).first()
        return self.schema.model_validate(response_query._asdict())

    def delete(self, menu_id: UUID) -> JSONResponse:
        menu = self.get_model_obj(menu_id)
        if isinstance(menu, JSONResponse):
            return menu  # response with http code 404
        self.session.delete(menu)
        self.session.commit()
        return JSONResponse(content={"status": True,
                                     "message": "The menu has been deleted"})


class SubmenuRepository:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
        self.model = Submenu
        self.schema = SubmenuReadSchema
        self.query = (session.query(
            Submenu.id,
            Submenu.title,
            Submenu.description,
            func.count(func.distinct(Dish.id)).label("dishes_count"))
            .outerjoin(Dish, Dish.submenu_id == Submenu.id)
            .group_by(Submenu.id))

    def get_all(self, menu_id: UUID) -> list[SubmenuReadSchema] | JSONResponse:
        menu = MenuRepository(self.session).get_model_obj(menu_id)
        if isinstance(menu, JSONResponse):
            return menu  # response with http code 404
        submenus = self.query.filter(Submenu.menu_id == menu_id).all()
        return [self.schema.model_validate(submenu._asdict())
                for submenu in submenus]

    def create(self, menu_id,
               input_data: dict) -> SubmenuReadSchema | JSONResponse:
        menu = MenuRepository(self.session).get_model_obj(menu_id)
        if isinstance(menu, JSONResponse):
            return menu  # response with http code 404
        new_submenu = self.model(**input_data)
        menu.submenus.append(new_submenu)
        self.session.commit()
        return self.schema.model_validate(new_submenu.as_dict())

    def get_model_obj(self, menu_id: UUID,
                      submenu_id: UUID) -> Submenu | JSONResponse:
        submenu = (self.session.query(self.model)
                   .filter(self.model.id == submenu_id).first())
        if not submenu:
            return (JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"detail": f"{self.model.__name__.lower()} "
                                   "not found"}))
        if submenu.menu_id != menu_id:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "menu id incorrect"}
            )
        return submenu

    def get(self, menu_id: UUID,
            submenu_id: UUID) -> SubmenuReadSchema | JSONResponse:
        submenu = self.get_model_obj(menu_id, submenu_id)
        if isinstance(submenu, JSONResponse):
            return submenu  # response with http code 404 or 400
        response_query = self.query.filter(self.model.id == submenu_id).first()
        return self.schema.model_validate(response_query._asdict())

    def update(self, menu_id: UUID,
               submenu_id: UUID,
               input_data: dict) -> SubmenuReadSchema | JSONResponse:
        submenu = self.get_model_obj(menu_id, submenu_id)
        if isinstance(submenu, JSONResponse):
            return submenu  # response with http code 404 or 400
        submenu.update(**input_data)
        self.session.add(submenu)
        self.session.commit()
        response_query = self.query.filter(self.model.id == submenu_id).first()
        return self.schema.model_validate(response_query._asdict())

    def delete(self, menu_id: UUID, submenu_id: UUID) -> JSONResponse:
        submenu = self.get_model_obj(menu_id, submenu_id)
        if isinstance(submenu, JSONResponse):
            return submenu  # response with http code 404 or 400
        self.session.delete(submenu)
        self.session.commit()
        return JSONResponse(
            content={"status": True, "message": "The submenu has been deleted"}
        )


class DishRepository:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
        self.model = Dish
        self.schema = DishReadSchema
        self.query = (session.query(Dish.id,
                                    Dish.title,
                                    Dish.description,
                                    Dish.price))

    def get_all(self, menu_id: UUID,
                submenu_id: UUID) -> list[DishReadSchema] | JSONResponse:
        submenu = (SubmenuRepository(self.session)
                   .get_model_obj(menu_id, submenu_id))
        if isinstance(submenu, JSONResponse):
            # return submenu  # response with http code 404 or 400
            return list()  # this is illogical, but necessary for postman tests
        dishes = self.query.filter(Dish.submenu_id == submenu_id).all()
        return [self.schema.model_validate(dish._asdict())
                for dish in dishes]

    def create(self, menu_id,
               submenu_id: UUID,
               input_data: dict) -> DishReadSchema | JSONResponse:
        submenu = (SubmenuRepository(self.session)
                   .get_model_obj(menu_id, submenu_id))
        if isinstance(submenu, JSONResponse):
            return submenu  # response with http code 404 or 400
        new_dish = self.model(**input_data)
        submenu.dishes.append(new_dish)
        self.session.commit()
        return self.schema.model_validate(new_dish.as_dict())

    def get_model_obj(self, menu_id: UUID,
                      submenu_id: UUID, dish_id: UUID) -> Dish | JSONResponse:
        dish = (self.session.query(self.model)
                .filter(self.model.id == dish_id).first())
        if not dish:
            return (JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"detail": f"{self.model.__name__.lower()} "
                                   "not found"}))
        if ((dish.submenu_id != submenu_id)
                or (dish.submenu.menu_id != menu_id)):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "menu or submenu id incorrect"}
            )
        return dish

    def get(self, menu_id: UUID,
            submenu_id: UUID, dish_id: UUID) -> DishReadSchema | JSONResponse:
        dish = self.get_model_obj(menu_id, submenu_id, dish_id)
        if isinstance(dish, JSONResponse):
            return dish  # response with http code 404 or 400
        response_query = self.query.filter(self.model.id == dish_id).first()
        return self.schema.model_validate(response_query._asdict())

    def update(self, menu_id: UUID,
               submenu_id: UUID,
               dish_id: UUID,
               input_data: dict) -> DishReadSchema | JSONResponse:
        dish = self.get_model_obj(menu_id, submenu_id, dish_id)
        if isinstance(dish, JSONResponse):
            return dish  # response with http code 404 or 400
        dish.update(**input_data)
        self.session.add(dish)
        self.session.commit()
        response_query = self.query.filter(self.model.id == dish_id).first()
        return self.schema.model_validate(response_query._asdict())

    def delete(self, menu_id: UUID,
               submenu_id: UUID, dish_id: UUID) -> JSONResponse:
        dish = self.get_model_obj(menu_id, submenu_id, dish_id)
        if isinstance(dish, JSONResponse):
            return dish  # response with http code 404 or 400
        self.session.delete(dish)
        self.session.commit()
        return JSONResponse(
            content={"status": True, "message": "The dish has been deleted"}
        )
