from uuid import UUID

from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from database import Session, get_session
from menus.repositories import (DishRepository, MenuRepository,
                                SubmenuRepository)
from menus.schemas import (DishReadSchema, DishWriteSchema, MenuReadSchema,
                           MenuWriteSchema, SubmenuReadSchema,
                           SubmenuWriteSchema)

router = APIRouter(prefix="/api/v1")


@router.get("/menus", status_code=status.HTTP_200_OK, tags=["Menus"])
def get_menus(session: Session = Depends(get_session)) -> list[MenuReadSchema]:
    return MenuRepository(session).get_all()


@router.post("/menus", status_code=status.HTTP_201_CREATED, tags=["Menus"])
def create_menu(menu_input: MenuWriteSchema,
                session: Session = Depends(get_session)) -> MenuReadSchema:
    return MenuRepository(session).create(menu_input.model_dump())


@router.get("/menus/{menu_id}",
            status_code=status.HTTP_200_OK, tags=["Menus"])
def get_menu(menu_id: UUID,
             session: Session = Depends(get_session)) -> MenuReadSchema:
    return MenuRepository(session).get(menu_id)


@router.patch("/menus/{menu_id}",
              status_code=status.HTTP_200_OK, tags=["Menus"])
def update_menu(menu_id: UUID, menu_input: MenuWriteSchema,
                session: Session = Depends(get_session)) -> MenuReadSchema:
    return MenuRepository(session).update(menu_id, menu_input.model_dump())


@router.delete("/menus/{menu_id}",
               status_code=status.HTTP_200_OK, tags=["Menus"])
def delete_menu(menu_id: UUID,
                session: Session = Depends(get_session)) -> JSONResponse:
    return MenuRepository(session).delete(menu_id)


@router.get("/menus/{menu_id}/submenus",
            status_code=status.HTTP_200_OK, tags=["Submenus"])
def get_submenus(menu_id: UUID,
                 session: Session = Depends(get_session)
                 ) -> list[SubmenuReadSchema]:
    return SubmenuRepository(session).get_all(menu_id)


@router.post("/menus/{menu_id}/submenus",
             status_code=status.HTTP_201_CREATED, tags=["Submenus"])
def create_submenu(menu_id: UUID,
                   submenu_input: SubmenuWriteSchema,
                   session: Session = Depends(get_session)
                   ) -> SubmenuReadSchema:
    return SubmenuRepository(session).create(menu_id,
                                             submenu_input.model_dump())


@router.get("/menus/{menu_id}/submenus/{submenu_id}",
            status_code=status.HTTP_200_OK, tags=["Submenus"])
def get_submenu(menu_id: UUID,
                submenu_id: UUID,
                session: Session = Depends(get_session)
                ) -> SubmenuReadSchema:
    return SubmenuRepository(session).get(menu_id, submenu_id)


@router.patch("/menus/{menu_id}/submenus/{submenu_id}",
              status_code=status.HTTP_200_OK, tags=["Submenus"])
def update_submenu(menu_id: UUID,
                   submenu_id: UUID,
                   submenu_input: SubmenuWriteSchema,
                   session: Session = Depends(get_session)
                   ) -> SubmenuReadSchema:
    return SubmenuRepository(session).update(menu_id,
                                             submenu_id,
                                             submenu_input.model_dump())


@router.delete("/menus/{menu_id}/submenus/{submenu_id}",
               status_code=status.HTTP_200_OK, tags=["Submenus"])
def delete_submenu(menu_id: UUID,
                   submenu_id: UUID,
                   session: Session = Depends(get_session)) -> JSONResponse:
    return SubmenuRepository(session).delete(menu_id, submenu_id)


@router.get("/menus/{menu_id}/submenus/{submenu_id}/dishes",
            status_code=status.HTTP_200_OK, tags=["Dishes"])
def get_dishes(menu_id: UUID,
               submenu_id: UUID,
               session: Session = Depends(get_session)
               ) -> list[DishReadSchema]:
    return DishRepository(session).get_all(menu_id, submenu_id)


@router.post("/menus/{menu_id}/submenus/{submenu_id}/dishes",
             status_code=status.HTTP_201_CREATED, tags=["Dishes"])
def create_dish(menu_id: UUID,
                submenu_id: UUID,
                dish_input: DishWriteSchema,
                session: Session = Depends(get_session)) -> DishReadSchema:
    return DishRepository(session).create(menu_id, submenu_id,
                                          dish_input.model_dump())


@router.get("/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
            status_code=status.HTTP_200_OK, tags=["Dishes"])
def get_dish(menu_id: UUID,
             submenu_id: UUID,
             dish_id: UUID,
             session: Session = Depends(get_session)) -> DishReadSchema:
    return DishRepository(session).get(menu_id, submenu_id, dish_id)


@router.patch("/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
              status_code=status.HTTP_200_OK, tags=["Dishes"])
def update_dish(menu_id: UUID,
                submenu_id: UUID,
                dish_id: UUID,
                dish_input: DishWriteSchema,
                session: Session = Depends(get_session)) -> DishReadSchema:
    return DishRepository(session).update(menu_id, submenu_id,
                                          dish_id, dish_input.model_dump())


@router.delete("/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
               status_code=status.HTTP_200_OK, tags=["Dishes"])
def delete_dish(menu_id: UUID,
                submenu_id: UUID,
                dish_id: UUID,
                session: Session = Depends(get_session)) -> JSONResponse:
    return DishRepository(session).delete(menu_id, submenu_id, dish_id)
