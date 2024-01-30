import uuid

from conftest import client
from data import (dish_expected_keys, dish_expected_values_404,
                  dish_request_body1, expected_keys_404, expected_keys_422,
                  menu_request_body1, submenu_request_body1)
from sqlalchemy.orm import Session
from starlette import status
from utils import check_keys, check_values

from menus.models import Dish, Menu, Submenu


def test_get_dishes_empty(test_session: Session):
    menu = Menu(**menu_request_body1)
    submenu = Submenu(**submenu_request_body1)
    menu.submenus.append(submenu)
    test_session.add(menu)
    test_session.commit()
    response = client.get(f"/menus/{str(menu.id)}"
                          f"/submenus/{str(submenu.id)}/dishes")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
    test_session.delete(menu)
    test_session.commit()


def test_create_dish(test_session: Session):
    menu = Menu(**menu_request_body1)
    submenu = Submenu(**submenu_request_body1)
    menu.submenus.append(submenu)
    test_session.add(menu)
    test_session.commit()
    expected_keys = dish_expected_keys
    expected_values = dish_request_body1
    response = client.post(f"/menus/{str(menu.id)}"
                           f"/submenus/{str(submenu.id)}/dishes",
                           json=dish_request_body1)
    assert response.status_code == status.HTTP_201_CREATED
    check_keys(response.json(), expected_keys)
    check_values(response.json(), expected_values)
    dish = (test_session.query(Dish)
            .filter(Dish.id == response.json().get("id")).first())
    assert dish, "Dish object not created!"
    check_values(dish.as_dict(), dish_request_body1)
    test_session.delete(menu)
    test_session.commit()


def test_create_dish_incorrect_body(test_session: Session):
    menu = Menu(**menu_request_body1)
    submenu = Submenu(**submenu_request_body1)
    menu.submenus.append(submenu)
    test_session.add(menu)
    test_session.commit()
    expected_keys = expected_keys_422
    request_body = {"incorrect_key1": 1, "incorrect_key2": 2}
    response = client.post(f"/menus/{str(menu.id)}"
                           f"/submenus/{str(submenu.id)}/dishes",
                           json=request_body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    check_keys(response.json(), expected_keys)
    test_session.delete(menu)
    test_session.commit()


def test_get_dishes_one_item(test_session: Session):
    menu = Menu(**menu_request_body1)
    submenu = Submenu(**submenu_request_body1)
    menu.submenus.append(submenu)
    dish = Dish(**dish_request_body1)
    submenu.dishes.append(dish)
    test_session.add(menu)
    test_session.commit()
    expected_keys = dish_expected_keys
    expected_values = dish_request_body1 | {"id": str(dish.id)}
    response = client.get(f"/menus/{str(menu.id)}"
                          f"/submenus/{str(submenu.id)}/dishes")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1, (f"Expected 1 dish item, "
                                       f"but got {len(response.json())}")
    check_keys(response.json()[0], expected_keys)
    check_values(response.json()[0], expected_values)
    test_session.delete(menu)
    test_session.commit()


def test_get_dish(test_session: Session):
    menu = Menu(**menu_request_body1)
    submenu = Submenu(**submenu_request_body1)
    menu.submenus.append(submenu)
    dish = Dish(**dish_request_body1)
    submenu.dishes.append(dish)
    test_session.add(menu)
    test_session.commit()
    expected_keys = dish_expected_keys
    expected_values = dish_request_body1 | {"id": str(dish.id)}
    response = client.get(f"/menus/{str(menu.id)}"
                          f"/submenus/{str(submenu.id)}"
                          f"/dishes/{str(dish.id)}")
    assert response.status_code == status.HTTP_200_OK
    check_keys(response.json(), expected_keys)
    check_values(response.json(), expected_values)
    test_session.delete(menu)
    test_session.commit()


def test_get_dish_404(test_session: Session):
    menu = Menu(**menu_request_body1)
    submenu = Submenu(**submenu_request_body1)
    menu.submenus.append(submenu)
    test_session.add(menu)
    test_session.commit()
    expected_keys = expected_keys_404
    expected_values = dish_expected_values_404
    response = client.get(f"/menus/{str(menu.id)}"
                          f"/submenus/{str(submenu.id)}"
                          f"/dishes/{uuid.uuid4()}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    check_keys(response.json(), expected_keys)
    check_values(response.json(), expected_values)
    test_session.delete(menu)
    test_session.commit()


def test_update_dish(test_session: Session):
    menu = Menu(**menu_request_body1)
    submenu = Submenu(**submenu_request_body1)
    menu.submenus.append(submenu)
    dish = Dish(**dish_request_body1)
    submenu.dishes.append(dish)
    test_session.add(menu)
    test_session.commit()
    expected_keys = dish_expected_keys
    new_request_body = {
        "title": "Dish changed",
        "description": "Dish description changed",
        "price": "100.00"
    }
    expected_values = new_request_body | {"id": str(dish.id)}
    response = client.patch(f"/menus/{str(menu.id)}"
                            f"/submenus/{str(submenu.id)}"
                            f"/dishes/{str(dish.id)}",
                            json=new_request_body)
    assert response.status_code == status.HTTP_200_OK
    check_keys(response.json(), expected_keys)
    check_values(response.json(), expected_values)
    test_session.delete(menu)
    test_session.commit()


def test_update_dish_incorrect_body(test_session: Session):
    menu = Menu(**menu_request_body1)
    submenu = Submenu(**submenu_request_body1)
    menu.submenus.append(submenu)
    dish = Dish(**dish_request_body1)
    submenu.dishes.append(dish)
    test_session.add(menu)
    test_session.commit()
    expected_keys = expected_keys_422
    request_body = {"incorrect_key1": 1, "incorrect_key2": 2}
    response = client.patch(f"/menus/{str(menu.id)}"
                            f"/submenus/{str(submenu.id)}"
                            f"/dishes/{str(dish.id)}",
                            json=request_body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    check_keys(response.json(), expected_keys)
    test_session.delete(menu)
    test_session.commit()


def test_update_dish_404(test_session: Session):
    menu = Menu(**menu_request_body1)
    submenu = Submenu(**submenu_request_body1)
    menu.submenus.append(submenu)
    dish = Dish(**dish_request_body1)
    submenu.dishes.append(dish)
    test_session.add(menu)
    test_session.commit()
    expected_keys = expected_keys_404
    expected_values = dish_expected_values_404
    new_request_body = {
        "title": "Dish changed",
        "description": "Dish description changed",
        "price": "100.00"
    }
    response = client.patch(f"/menus/{str(menu.id)}"
                            f"/submenus/{str(submenu.id)}"
                            f"/dishes/{uuid.uuid4()}",
                            json=new_request_body)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    check_keys(response.json(), expected_keys)
    check_values(response.json(), expected_values)
    test_session.delete(menu)
    test_session.commit()


def test_delete_dish(test_session: Session):
    menu = Menu(**menu_request_body1)
    submenu = Submenu(**submenu_request_body1)
    menu.submenus.append(submenu)
    dish = Dish(**dish_request_body1)
    submenu.dishes.append(dish)
    test_session.add(menu)
    test_session.commit()
    expected_keys = ["status", "message"]
    expected_values = {"status": True,
                       "message": "The dish has been deleted"}
    response = client.delete(f"/menus/{str(menu.id)}"
                             f"/submenus/{str(submenu.id)}"
                             f"/dishes/{str(dish.id)}")
    assert response.status_code == status.HTTP_200_OK
    check_keys(response.json(), expected_keys)
    check_values(response.json(), expected_values)
    dish = test_session.query(Dish).filter(Dish.id == dish.id).first()
    assert not dish, "Dish object was not deleted!"
    test_session.delete(menu)
    test_session.commit()


def test_delete_dish_404(test_session: Session):
    menu = Menu(**menu_request_body1)
    submenu = Submenu(**submenu_request_body1)
    menu.submenus.append(submenu)
    test_session.add(menu)
    test_session.commit()
    expected_keys = expected_keys_404
    expected_values = dish_expected_values_404
    response = client.delete(f"/menus/{str(menu.id)}"
                             f"/submenus/{str(submenu.id)}"
                             f"/dishes/{uuid.uuid4()}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    check_keys(response.json(), expected_keys)
    check_values(response.json(), expected_values)
    test_session.delete(menu)
    test_session.commit()
