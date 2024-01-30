import uuid

from conftest import client
from data import (expected_keys_404, expected_keys_422, menu_expected_keys,
                  menu_expected_values_404, menu_request_body1)
from sqlalchemy.orm import Session
from starlette import status
from utils import check_keys, check_values

from menus.models import Menu


def test_get_menus_empty():
    response = client.get("/menus")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_create_menu(test_session: Session):
    expected_keys = menu_expected_keys
    expected_values = menu_request_body1 | {"submenus_count": 0,
                                            "dishes_count": 0}
    response = client.post("/menus", json=menu_request_body1)
    assert response.status_code == status.HTTP_201_CREATED
    check_keys(response.json(), expected_keys)
    check_values(response.json(), expected_values)
    menu = (test_session.query(Menu)
            .filter(Menu.id == response.json().get("id")).first())
    assert menu, "Menu object not created!"
    check_values(menu.as_dict(), menu_request_body1)
    test_session.delete(menu)
    test_session.commit()


def test_create_menu_incorrect_body():
    expected_keys = expected_keys_422
    request_body = {"incorrect_key1": 1, "incorrect_key2": 2}
    response = client.post("/menus", json=request_body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    check_keys(response.json(), expected_keys)


def test_get_menus_one_item(test_session: Session):
    menu = Menu(**menu_request_body1)
    test_session.add(menu)
    test_session.commit()
    expected_keys = menu_expected_keys
    expected_values = menu_request_body1 | {"submenus_count": 0,
                                            "dishes_count": 0,
                                            "id": str(menu.id)}
    response = client.get("/menus")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1, (f"Expected 1 menu item, "
                                       f"but got {len(response.json())}")
    check_keys(response.json()[0], expected_keys)
    check_values(response.json()[0], expected_values)
    test_session.delete(menu)
    test_session.commit()


def test_get_menu(test_session: Session):
    menu = Menu(**menu_request_body1)
    test_session.add(menu)
    test_session.commit()
    expected_keys = menu_expected_keys
    expected_values = menu_request_body1 | {"submenus_count": 0,
                                            "dishes_count": 0,
                                            "id": str(menu.id)}
    response = client.get(f"/menus/{str(menu.id)}")
    assert response.status_code == status.HTTP_200_OK
    check_keys(response.json(), expected_keys)
    check_values(response.json(), expected_values)
    test_session.delete(menu)
    test_session.commit()


def test_get_menu_404():
    expected_keys = expected_keys_404
    expected_values = menu_expected_values_404
    response = client.get(f"/menus/{uuid.uuid4()}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    check_keys(response.json(), expected_keys)
    check_values(response.json(), expected_values)


def test_update_menu(test_session: Session):
    menu = Menu(**menu_request_body1)
    test_session.add(menu)
    test_session.commit()
    expected_keys = menu_expected_keys
    new_request_body = {
        "title": "Menu changed",
        "description": "Menu description changed"
    }
    expected_values = new_request_body | {"submenus_count": 0,
                                          "dishes_count": 0,
                                          "id": str(menu.id)}
    response = client.patch(f"/menus/{str(menu.id)}", json=new_request_body)
    assert response.status_code == status.HTTP_200_OK
    check_keys(response.json(), expected_keys)
    check_values(response.json(), expected_values)
    test_session.refresh(menu)
    check_values(menu.as_dict(), new_request_body)
    test_session.delete(menu)
    test_session.commit()


def test_update_menu_incorrect_body(test_session: Session):
    menu = Menu(**menu_request_body1)
    test_session.add(menu)
    test_session.commit()
    expected_keys = expected_keys_422
    request_body = {"incorrect_key1": 1, "incorrect_key2": 2}
    response = client.patch(f"/menus/{str(menu.id)}", json=request_body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    check_keys(response.json(), expected_keys)
    test_session.delete(menu)
    test_session.commit()


def test_update_menu_404():
    expected_keys = expected_keys_404
    expected_values = menu_expected_values_404
    new_request_body = {
        "title": "Menu changed",
        "description": "Menu description changed"
    }
    response = client.patch(f"/menus/{uuid.uuid4()}", json=new_request_body)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    check_keys(response.json(), expected_keys)
    check_values(response.json(), expected_values)


def test_delete_menu(test_session: Session):
    menu = Menu(**menu_request_body1)
    test_session.add(menu)
    test_session.commit()
    expected_keys = ["status", "message"]
    expected_values = {"status": True,
                       "message": "The menu has been deleted"}
    response = client.delete(f"/menus/{str(menu.id)}")
    assert response.status_code == status.HTTP_200_OK
    check_keys(response.json(), expected_keys)
    check_values(response.json(), expected_values)
    menu = test_session.query(Menu).filter(Menu.id == menu.id).first()
    assert not menu, "Menu object was not deleted!"


def test_delete_menu_404():
    expected_keys = expected_keys_404
    expected_values = menu_expected_values_404
    response = client.delete(f"/menus/{uuid.uuid4()}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    check_keys(response.json(), expected_keys)
    check_values(response.json(), expected_values)
