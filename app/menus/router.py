from uuid import UUID

from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from database import Session, get_session
from menus.models import Dish, Menu, Submenu
from menus.schemas import (DishReadSchema, DishWriteSchema, MenuReadSchema,
                           MenuWriteSchema, SubmenuReadSchema,
                           SubmenuWriteSchema)
from menus.utils.jsonresponse404 import JSONResponse404

router = APIRouter(prefix="/api/v1")


@router.get("/menus", status_code=status.HTTP_200_OK, tags=["Menus"])
def get_menus(session: Session = Depends(get_session)) -> list[MenuReadSchema]:
    return Menu.get_schema_objects(session)


@router.post("/menus", status_code=status.HTTP_201_CREATED, tags=["Menus"])
def create_menu(menu_input: MenuWriteSchema,
                session: Session = Depends(get_session)) -> MenuReadSchema:
    new_menu = Menu(**menu_input.model_dump())
    session.add(new_menu)
    session.commit()
    return new_menu


@router.get("/menus/{menu_id}",
            status_code=status.HTTP_200_OK, tags=["Menus"])
def get_menu(menu_id: UUID,
             session: Session = Depends(get_session)) -> MenuReadSchema:
    return Menu.get_schema_obj_or_404(session, menu_id)


@router.patch("/menus/{menu_id}",
              status_code=status.HTTP_200_OK, tags=["Menus"])
def update_menu(menu_id: UUID, menu_input: MenuWriteSchema,
                session: Session = Depends(get_session)) -> MenuReadSchema:
    menu = Menu.get_or_404(session, menu_id)
    if menu.__class__ is JSONResponse404:
        return menu  # response with http code 404
    menu.update(**menu_input.model_dump())
    session.add(menu)
    session.commit()
    return Menu.get_schema_obj_or_404(session, menu_id)


@router.delete("/menus/{menu_id}",
               status_code=status.HTTP_200_OK, tags=["Menus"])
def delete_menu(menu_id: UUID,
                session: Session = Depends(get_session)) -> JSONResponse:
    menu = Menu.get_or_404(session, menu_id)
    if menu.__class__ is JSONResponse404:
        return menu  # response with http code 404
    session.delete(menu)
    session.commit()
    return JSONResponse(content={"status": True,
                                 "message": "The menu has been deleted"})


@router.get("/menus/{menu_id}/submenus",
            status_code=status.HTTP_200_OK, tags=["Submenus"])
def get_submenus(menu_id: UUID,
                 session: Session = Depends(get_session)
                 ) -> list[SubmenuReadSchema]:
    menu = Menu.get_or_404(session, menu_id)
    if menu.__class__ is JSONResponse404:
        return menu  # response with http code 404
    return Submenu.get_schema_objects_by_menu(session, menu_id)


@router.post("/menus/{menu_id}/submenus",
             status_code=status.HTTP_201_CREATED, tags=["Submenus"])
def create_submenu(menu_id: UUID,
                   submenu_input: SubmenuWriteSchema,
                   session: Session = Depends(get_session)
                   ) -> SubmenuReadSchema:
    menu = Menu.get_or_404(session, menu_id)
    if menu.__class__ is JSONResponse404:
        return menu  # response with http code 404
    new_submenu = Submenu(**submenu_input.model_dump())
    menu.submenus.append(new_submenu)
    session.commit()
    return new_submenu


@router.get("/menus/{menu_id}/submenus/{submenu_id}",
            status_code=status.HTTP_200_OK, tags=["Submenus"])
def get_submenu(menu_id: UUID,
                submenu_id: UUID,
                session: Session = Depends(get_session)
                ) -> SubmenuReadSchema:
    submenu = Submenu.get_or_404(session, submenu_id)
    if submenu.__class__ is JSONResponse404:
        return submenu  # response with http code 404
    if not submenu.check_parent_menu(menu_id):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "menu id incorrect"}
        )
    return Submenu.get_schema_obj_or_404(session, submenu_id)


@router.patch("/menus/{menu_id}/submenus/{submenu_id}",
              status_code=status.HTTP_200_OK, tags=["Submenus"])
def update_submenu(menu_id: UUID,
                   submenu_id: UUID,
                   submenu_input: SubmenuWriteSchema,
                   session: Session = Depends(get_session)
                   ) -> SubmenuReadSchema:
    submenu = Submenu.get_or_404(session, submenu_id)
    if submenu.__class__ is JSONResponse404:
        return submenu  # response with http code 404
    if not submenu.check_parent_menu(menu_id):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "menu id incorrect"}
        )
    submenu.update(**submenu_input.model_dump())
    session.add(submenu)
    session.commit()
    return Submenu.get_schema_obj_or_404(session, submenu_id)


@router.delete("/menus/{menu_id}/submenus/{submenu_id}",
               status_code=status.HTTP_200_OK, tags=["Submenus"])
def delete_submenu(menu_id: UUID,
                   submenu_id: UUID,
                   session: Session = Depends(get_session)) -> JSONResponse:
    submenu = Submenu.get_or_404(session, submenu_id)
    if submenu.__class__ is JSONResponse404:
        return submenu  # response with http code 404
    if not submenu.check_parent_menu(menu_id):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "menu id incorrect"}
        )
    session.delete(submenu)
    session.commit()
    return JSONResponse(content={"status": True,
                                 "message": "The submenu has been deleted"})


@router.get("/menus/{menu_id}/submenus/{submenu_id}/dishes",
            status_code=status.HTTP_200_OK, tags=["Dishes"])
def get_dishes(menu_id: UUID,
               submenu_id: UUID,
               session: Session = Depends(get_session)
               ) -> list[DishReadSchema]:
    submenu = Submenu.get_or_404(session, submenu_id)
    if submenu.__class__ is JSONResponse404:
        # return submenu  # response with http code 404
        return list()  # this is illogical, but necessary for postman tests
    if not submenu.check_parent_menu(menu_id):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "menu id incorrect"}
        )
    return Dish.get_schema_objects_by_submenu(session, submenu_id)


@router.post("/menus/{menu_id}/submenus/{submenu_id}/dishes",
             status_code=status.HTTP_201_CREATED, tags=["Dishes"])
def create_dish(menu_id: UUID,
                submenu_id: UUID,
                dish_input: DishWriteSchema,
                session: Session = Depends(get_session)) -> DishReadSchema:
    submenu = Submenu.get_or_404(session, submenu_id)
    if submenu.__class__ is JSONResponse404:
        return submenu  # response with http code 404
    if not submenu.check_parent_menu(menu_id):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "menu id incorrect"}
        )
    new_dish = Dish(**dish_input.model_dump())
    submenu.dishes.append(new_dish)
    session.commit()
    return new_dish


@router.get("/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
            status_code=status.HTTP_200_OK, tags=["Dishes"])
def get_dish(menu_id: UUID,
             submenu_id: UUID,
             dish_id: UUID,
             session: Session = Depends(get_session)) -> DishReadSchema:
    dish = Dish.get_or_404(session, dish_id)
    if dish.__class__ is JSONResponse404:
        return dish  # response with http code 404
    if not ((dish.check_parent_submenu(submenu_id)
             and dish.submenu.check_parent_menu(menu_id))):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "menu or submenu id incorrect"}
        )
    return dish


@router.patch("/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
              status_code=status.HTTP_200_OK, tags=["Dishes"])
def update_dish(menu_id: UUID,
                submenu_id: UUID,
                dish_id: UUID,
                dish_input: DishWriteSchema,
                session: Session = Depends(get_session)) -> DishReadSchema:
    dish = Dish.get_or_404(session, dish_id)
    if dish.__class__ is JSONResponse404:
        return dish  # response with http code 404
    if not ((dish.check_parent_submenu(submenu_id)
             and dish.submenu.check_parent_menu(menu_id))):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "menu or submenu id incorrect"}
        )
    dish.update(**dish_input.model_dump())
    session.add(dish)
    session.commit()
    return dish


@router.delete("/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
               status_code=status.HTTP_200_OK, tags=["Dishes"])
def delete_dish(menu_id: UUID,
                submenu_id: UUID,
                dish_id: UUID,
                session: Session = Depends(get_session)) -> JSONResponse:
    dish = Dish.get_or_404(session, dish_id)
    if dish.__class__ is JSONResponse404:
        return dish  # response with http code 404
    if not ((dish.check_parent_submenu(submenu_id)
             and dish.submenu.check_parent_menu(menu_id))):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "menu or submenu id incorrect"}
        )
    session.delete(dish)
    session.commit()
    return JSONResponse(content={"status": True,
                                 "message": "The dish has been deleted"})
