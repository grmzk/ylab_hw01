import uuid

from starlette import status

from conftest import client
from data import (expected_keys_404, expected_keys_422, menu_expected_keys,
                  menu_expected_values_404, menu_request_body1)
from utils import check_json_keys, check_json_values

last_inserted_menu_id: uuid = None


def test_get_menus_empty():
    response = client.get("/menus")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_create_menu():
    global last_inserted_menu_id
    expected_keys = menu_expected_keys
    expected_values = menu_request_body1 | {"submenus_count": 0,
                                            "dishes_count": 0}
    response = client.post("/menus", json=menu_request_body1)
    assert response.status_code == status.HTTP_201_CREATED
    check_json_keys(response.json(), expected_keys)
    check_json_values(response.json(), expected_values)
    last_inserted_menu_id = response.json()["id"]


def test_create_menu_incorrect_body():
    expected_keys = expected_keys_422
    request_body = {"incorrect_key1": 1, "incorrect_key2": 2}
    response = client.post("/menus", json=request_body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    check_json_keys(response.json(), expected_keys)


def test_get_menus_one_item():
    expected_keys = menu_expected_keys
    expected_values = menu_request_body1 | {"submenus_count": 0,
                                            "dishes_count": 0,
                                            "id": last_inserted_menu_id}
    response = client.get("/menus")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1, (f"Expected 1 menu item, "
                                       f"but got {len(response)}")
    check_json_keys(response.json()[0], expected_keys)
    check_json_values(response.json()[0], expected_values)


def test_get_menu():
    expected_keys = menu_expected_keys
    expected_values = menu_request_body1 | {"submenus_count": 0,
                                            "dishes_count": 0,
                                            "id": last_inserted_menu_id}
    response = client.get(f"/menus/{last_inserted_menu_id}")
    assert response.status_code == status.HTTP_200_OK
    check_json_keys(response.json(), expected_keys)
    check_json_values(response.json(), expected_values)


def test_get_menu_404():
    expected_keys = expected_keys_404
    expected_values = menu_expected_values_404
    response = client.get(f"/menus/{uuid.uuid4()}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    check_json_keys(response.json(), expected_keys)
    check_json_values(response.json(), expected_values)


def test_update_menu():
    expected_keys = menu_expected_keys
    new_request_body = {
        "title": "Menu changed",
        "description": "Menu description changed"
    }
    expected_values = new_request_body | {"submenus_count": 0,
                                          "dishes_count": 0,
                                          "id": last_inserted_menu_id}
    response = client.patch(f"/menus/{last_inserted_menu_id}",
                            json=new_request_body)
    assert response.status_code == status.HTTP_200_OK
    check_json_keys(response.json(), expected_keys)
    check_json_values(response.json(), expected_values)


def test_update_menu_incorrect_body():
    expected_keys = expected_keys_422
    request_body = {"incorrect_key1": 1, "incorrect_key2": 2}
    response = client.patch(f"/menus/{last_inserted_menu_id}",
                            json=request_body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    check_json_keys(response.json(), expected_keys)


def test_update_menu_404():
    expected_keys = expected_keys_404
    expected_values = menu_expected_values_404
    new_request_body = {
        "title": "Menu changed",
        "description": "Menu description changed"
    }
    response = client.patch(f"/menus/{uuid.uuid4()}", json=new_request_body)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    check_json_keys(response.json(), expected_keys)
    check_json_values(response.json(), expected_values)


def test_delete_menu():
    expected_keys = ["status", "message"]
    expected_values = {"status": True,
                       "message": "The menu has been deleted"}
    response = client.delete(f"/menus/{last_inserted_menu_id}")
    assert response.status_code == status.HTTP_200_OK
    check_json_keys(response.json(), expected_keys)
    check_json_values(response.json(), expected_values)
    test_get_menus_empty()


def test_delete_menu_404():
    expected_keys = expected_keys_404
    expected_values = menu_expected_values_404
    response = client.delete(f"/menus/{last_inserted_menu_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    check_json_keys(response.json(), expected_keys)
    check_json_values(response.json(), expected_values)
