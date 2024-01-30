import uuid

from conftest import client
from data import (expected_keys_404, expected_keys_422, menu_request_body1,
                  submenu_expected_keys, submenu_expected_values_404,
                  submenu_request_body1)
from sqlalchemy.orm import Session
from starlette import status
from utils import check_keys, check_values

from menus.models import Menu, Submenu


def test_get_submenus_empty(test_session: Session):
    menu = Menu(**menu_request_body1)
    test_session.add(menu)
    test_session.commit()
    response = client.get(f"/menus/{str(menu.id)}/submenus")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
    test_session.delete(menu)
    test_session.commit()


def test_create_submenu(test_session: Session):
    menu = Menu(**menu_request_body1)
    test_session.add(menu)
    test_session.commit()
    expected_keys = submenu_expected_keys
    expected_values = submenu_request_body1 | {"dishes_count": 0}
    response = client.post(f"/menus/{str(menu.id)}/submenus",
                           json=submenu_request_body1)
    assert response.status_code == status.HTTP_201_CREATED
    check_keys(response.json(), expected_keys)
    check_values(response.json(), expected_values)
    submenu = (test_session.query(Submenu)
               .filter(Submenu.id == response.json().get("id")).first())
    assert submenu, "Submenu object not created!"
    check_values(submenu.as_dict(), submenu_request_body1)
    test_session.delete(menu)
    test_session.commit()


def test_create_submenu_incorrect_body(test_session: Session):
    menu = Menu(**menu_request_body1)
    test_session.add(menu)
    test_session.commit()
    expected_keys = expected_keys_422
    request_body = {"incorrect_key1": 1, "incorrect_key2": 2}
    response = client.post(f"/menus/{str(menu.id)}/submenus",
                           json=request_body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    check_keys(response.json(), expected_keys)
    test_session.delete(menu)
    test_session.commit()


def test_get_submenus_one_item(test_session: Session):
    menu = Menu(**menu_request_body1)
    submenu = Submenu(**submenu_request_body1)
    menu.submenus.append(submenu)
    test_session.add(menu)
    test_session.commit()
    expected_keys = submenu_expected_keys
    expected_values = submenu_request_body1 | {"dishes_count": 0,
                                               "id": str(submenu.id)}
    response = client.get(f"/menus/{str(menu.id)}/submenus")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1, (f"Expected 1 submenu item, "
                                       f"but got {len(response.json())}")
    check_keys(response.json()[0], expected_keys)
    check_values(response.json()[0], expected_values)
    test_session.delete(menu)
    test_session.commit()


def test_get_submenu(test_session: Session):
    menu = Menu(**menu_request_body1)
    submenu = Submenu(**submenu_request_body1)
    menu.submenus.append(submenu)
    test_session.add(menu)
    test_session.commit()
    expected_keys = submenu_expected_keys
    expected_values = submenu_request_body1 | {"dishes_count": 0,
                                               "id": str(submenu.id)}
    response = client.get(f"/menus/{str(menu.id)}"
                          f"/submenus/{str(submenu.id)}")
    assert response.status_code == status.HTTP_200_OK
    check_keys(response.json(), expected_keys)
    check_values(response.json(), expected_values)
    test_session.delete(menu)
    test_session.commit()


def test_get_submenu_404(test_session: Session):
    menu = Menu(**menu_request_body1)
    test_session.add(menu)
    test_session.commit()
    expected_keys = expected_keys_404
    expected_values = submenu_expected_values_404
    response = client.get(f"/menus/{str(menu.id)}"
                          f"/submenus/{uuid.uuid4()}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    check_keys(response.json(), expected_keys)
    check_values(response.json(), expected_values)
    test_session.delete(menu)
    test_session.commit()


def test_update_submenu(test_session: Session):
    menu = Menu(**menu_request_body1)
    submenu = Submenu(**submenu_request_body1)
    menu.submenus.append(submenu)
    test_session.add(menu)
    test_session.commit()
    expected_keys = submenu_expected_keys
    new_request_body = {
        "title": "Submenu changed",
        "description": "Submenu description changed"
    }
    expected_values = new_request_body | {"dishes_count": 0,
                                          "id": str(submenu.id)}
    response = client.patch(f"/menus/{str(menu.id)}"
                            f"/submenus/{str(submenu.id)}",
                            json=new_request_body)
    assert response.status_code == status.HTTP_200_OK
    check_keys(response.json(), expected_keys)
    check_values(response.json(), expected_values)
    test_session.refresh(submenu)
    check_values(submenu.as_dict(), new_request_body)
    test_session.delete(menu)
    test_session.commit()


def test_update_submenu_incorrect_body(test_session: Session):
    menu = Menu(**menu_request_body1)
    submenu = Submenu(**submenu_request_body1)
    menu.submenus.append(submenu)
    test_session.add(menu)
    test_session.commit()
    expected_keys = expected_keys_422
    request_body = {"incorrect_key1": 1, "incorrect_key2": 2}
    response = client.patch(f"/menus/{str(menu.id)}"
                            f"/submenus/{str(submenu.id)}",
                            json=request_body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    check_keys(response.json(), expected_keys)
    test_session.delete(menu)
    test_session.commit()


def test_update_submenu_404(test_session: Session):
    menu = Menu(**menu_request_body1)
    test_session.add(menu)
    test_session.commit()
    expected_keys = expected_keys_404
    expected_values = submenu_expected_values_404
    new_request_body = {
        "title": "Submenu changed",
        "description": "Submenu description changed"
    }
    response = client.patch(f"/menus/{str(menu.id)}"
                            f"/submenus/{uuid.uuid4()}",
                            json=new_request_body)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    check_keys(response.json(), expected_keys)
    check_values(response.json(), expected_values)
    test_session.delete(menu)
    test_session.commit()


def test_delete_submenu(test_session: Session):
    menu = Menu(**menu_request_body1)
    submenu = Submenu(**submenu_request_body1)
    menu.submenus.append(submenu)
    test_session.add(menu)
    test_session.commit()
    expected_keys = ["status", "message"]
    expected_values = {"status": True,
                       "message": "The submenu has been deleted"}
    response = client.delete(f"/menus/{str(menu.id)}"
                             f"/submenus/{str(submenu.id)}")
    assert response.status_code == status.HTTP_200_OK
    check_keys(response.json(), expected_keys)
    check_values(response.json(), expected_values)
    submenu = (
        test_session.query(Submenu).filter(Submenu.id == submenu.id).first()
    )
    assert not submenu, "Submenu object was not deleted!"
    test_session.delete(menu)
    test_session.commit()


def test_delete_submenu_404(test_session: Session):
    menu = Menu(**menu_request_body1)
    test_session.add(menu)
    test_session.commit()
    expected_keys = expected_keys_404
    expected_values = submenu_expected_values_404
    response = client.delete(f"/menus/{str(menu.id)}"
                             f"/submenus/{uuid.uuid4()}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    check_keys(response.json(), expected_keys)
    check_values(response.json(), expected_values)
    test_session.delete(menu)
    test_session.commit()
