from conftest import client
from data import (dish_request_body1, dish_request_body2, dish_request_body3,
                  menu_request_body1, menu_request_body2, menu_request_body3,
                  submenu_request_body1, submenu_request_body2,
                  submenu_request_body3)
from sqlalchemy.orm import Session

from menus.models import Dish, Menu, Submenu


def test_menu_submenus_count_zero(test_session: Session):
    menu1 = Menu(**menu_request_body1)
    menu2 = Menu(**menu_request_body2)
    menu3 = Menu(**menu_request_body3)
    test_session.add_all([menu1, menu2, menu3])
    test_session.commit()
    for menu in (menu1, menu2, menu3):
        response = client.get(f"/menus/{menu.id}")
        assert response.json()["submenus_count"] == 0
    test_session.delete(menu1)
    test_session.delete(menu2)
    test_session.delete(menu3)
    test_session.commit()


def test_menu_dishes_count_zero(test_session: Session):
    menu1 = Menu(**menu_request_body1)
    menu2 = Menu(**menu_request_body2)
    menu3 = Menu(**menu_request_body3)
    test_session.add_all([menu1, menu2, menu3])
    test_session.commit()
    for menu in (menu1, menu2, menu3):
        response = client.get(f"/menus/{menu.id}")
        assert response.json()["dishes_count"] == 0
    test_session.delete(menu1)
    test_session.delete(menu2)
    test_session.delete(menu3)
    test_session.commit()


def test_menu_submenus_count(test_session: Session):
    menu1 = Menu(**menu_request_body1)
    submenu1 = Submenu(**submenu_request_body1)
    submenu2 = Submenu(**submenu_request_body2)
    menu1.submenus.append(submenu1)
    menu1.submenus.append(submenu2)
    menu2 = Menu(**menu_request_body2)
    submenu3 = Submenu(**submenu_request_body3)
    menu2.submenus.append(submenu3)
    menu3 = Menu(**menu_request_body3)
    test_session.add_all([menu1, menu2, menu3])
    test_session.commit()
    response = client.get(f"/menus/{menu1.id}")
    assert response.json()["submenus_count"] == 2
    response = client.get(f"/menus/{menu2.id}")
    assert response.json()["submenus_count"] == 1
    response = client.get(f"/menus/{menu3.id}")
    assert response.json()["submenus_count"] == 0
    test_session.delete(menu1)
    test_session.delete(menu2)
    test_session.delete(menu3)
    test_session.commit()


def test_menu_dishes_count(test_session: Session):
    menu1 = Menu(**menu_request_body1)
    submenu1 = Submenu(**submenu_request_body1)
    dish1 = Dish(**dish_request_body1)
    dish2 = Dish(**dish_request_body2)
    submenu1.dishes.append(dish1)
    submenu1.dishes.append(dish2)
    submenu2 = Submenu(**submenu_request_body2)
    dish3 = Dish(**dish_request_body3)
    submenu2.dishes.append(dish3)
    menu1.submenus.append(submenu1)
    menu1.submenus.append(submenu2)
    menu2 = Menu(**menu_request_body2)
    submenu3 = Submenu(**submenu_request_body3)
    menu2.submenus.append(submenu3)
    menu3 = Menu(**menu_request_body3)
    test_session.add_all([menu1, menu2, menu3])
    test_session.commit()
    response = client.get(f"/menus/{menu1.id}")
    assert response.json()["dishes_count"] == 3
    response = client.get(f"/menus/{menu2.id}")
    assert response.json()["dishes_count"] == 0
    response = client.get(f"/menus/{menu3.id}")
    assert response.json()["dishes_count"] == 0
    test_session.delete(menu1)
    test_session.delete(menu2)
    test_session.delete(menu3)
    test_session.commit()


def test_submenu_dishes_count(test_session: Session):
    menu1 = Menu(**menu_request_body1)
    submenu1 = Submenu(**submenu_request_body1)
    dish1 = Dish(**dish_request_body1)
    dish2 = Dish(**dish_request_body2)
    submenu1.dishes.append(dish1)
    submenu1.dishes.append(dish2)
    submenu2 = Submenu(**submenu_request_body2)
    dish3 = Dish(**dish_request_body3)
    submenu2.dishes.append(dish3)
    menu1.submenus.append(submenu1)
    menu1.submenus.append(submenu2)
    menu2 = Menu(**menu_request_body2)
    submenu3 = Submenu(**submenu_request_body3)
    menu2.submenus.append(submenu3)
    menu3 = Menu(**menu_request_body3)
    test_session.add_all([menu1, menu2, menu3])
    test_session.commit()
    response = client.get(f"/menus/{menu1.id}/submenus/{submenu1.id}")
    assert response.json()["dishes_count"] == 2
    response = client.get(f"/menus/{menu1.id}/submenus/{submenu2.id}")
    assert response.json()["dishes_count"] == 1
    response = client.get(f"/menus/{menu2.id}/submenus/{submenu3.id}")
    assert response.json()["dishes_count"] == 0
    test_session.delete(menu1)
    test_session.delete(menu2)
    test_session.delete(menu3)
    test_session.commit()


def test_menu_submenus_count_after_submenu_delete(test_session: Session):
    menu1 = Menu(**menu_request_body1)
    submenu1 = Submenu(**submenu_request_body1)
    dish1 = Dish(**dish_request_body1)
    dish2 = Dish(**dish_request_body2)
    submenu1.dishes.append(dish1)
    submenu1.dishes.append(dish2)
    submenu2 = Submenu(**submenu_request_body2)
    dish3 = Dish(**dish_request_body3)
    submenu2.dishes.append(dish3)
    menu1.submenus.append(submenu1)
    menu1.submenus.append(submenu2)
    test_session.add(menu1)
    test_session.commit()
    response = client.get(f"/menus/{menu1.id}")
    assert response.json()["submenus_count"] == 2
    test_session.delete(submenu1)
    test_session.commit()
    response = client.get(f"/menus/{menu1.id}")
    assert response.json()["submenus_count"] == 1
    test_session.delete(menu1)
    test_session.commit()


def test_menu_dishes_count_after_submenu_delete(test_session: Session):
    menu1 = Menu(**menu_request_body1)
    submenu1 = Submenu(**submenu_request_body1)
    dish1 = Dish(**dish_request_body1)
    dish2 = Dish(**dish_request_body2)
    submenu1.dishes.append(dish1)
    submenu1.dishes.append(dish2)
    submenu2 = Submenu(**submenu_request_body2)
    dish3 = Dish(**dish_request_body3)
    submenu2.dishes.append(dish3)
    menu1.submenus.append(submenu1)
    menu1.submenus.append(submenu2)
    test_session.add(menu1)
    test_session.commit()
    response = client.get(f"/menus/{menu1.id}")
    assert response.json()["dishes_count"] == 3
    test_session.delete(submenu1)
    test_session.commit()
    response = client.get(f"/menus/{menu1.id}")
    assert response.json()["dishes_count"] == 1
    test_session.delete(menu1)
    test_session.commit()
