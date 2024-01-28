import uuid

from starlette import status

from conftest import client
from data import (expected_keys_404, expected_keys_422, menu_request_body1,
                  submenu_expected_keys, submenu_expected_values_404,
                  submenu_request_body1)
from utils import check_json_keys, check_json_values

last_inserted_menu_id: uuid = None
last_inserted_submenu_id: uuid = None


def test_get_submenus_empty():
    global last_inserted_menu_id
    response = client.post("/menus", json=menu_request_body1)
    last_inserted_menu_id = response.json()["id"]
    response = client.get(f"/menus/{last_inserted_menu_id}/submenus")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_create_submenu():
    global last_inserted_submenu_id
    expected_keys = submenu_expected_keys
    expected_values = submenu_request_body1 | {"dishes_count": 0}
    response = client.post(f"/menus/{last_inserted_menu_id}/submenus",
                           json=submenu_request_body1)
    assert response.status_code == status.HTTP_201_CREATED
    check_json_keys(response.json(), expected_keys)
    check_json_values(response.json(), expected_values)
    last_inserted_submenu_id = response.json()["id"]


def test_create_submenu_incorrect_body():
    expected_keys = expected_keys_422
    request_body = {"incorrect_key1": 1, "incorrect_key2": 2}
    response = client.post(f"/menus/{last_inserted_menu_id}/submenus",
                           json=request_body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    check_json_keys(response.json(), expected_keys)


def test_get_submenus_one_item():
    expected_keys = submenu_expected_keys
    expected_values = submenu_request_body1 | {"dishes_count": 0,
                                               "id": last_inserted_submenu_id}
    response = client.get(f"/menus/{last_inserted_menu_id}/submenus")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1, (f"Expected 1 submenu item, "
                                       f"but got {len(response)}")
    check_json_keys(response.json()[0], expected_keys)
    check_json_values(response.json()[0], expected_values)


def test_get_submenu():
    expected_keys = submenu_expected_keys
    expected_values = submenu_request_body1 | {"dishes_count": 0,
                                               "id": last_inserted_submenu_id}
    response = client.get(f"/menus/{last_inserted_menu_id}"
                          f"/submenus/{last_inserted_submenu_id}")
    assert response.status_code == status.HTTP_200_OK
    check_json_keys(response.json(), expected_keys)
    check_json_values(response.json(), expected_values)


def test_get_submenu_404():
    expected_keys = expected_keys_404
    expected_values = submenu_expected_values_404
    response = client.get(f"/menus/{last_inserted_menu_id}"
                          f"/submenus/{uuid.uuid4()}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    check_json_keys(response.json(), expected_keys)
    check_json_values(response.json(), expected_values)


def test_update_submenu():
    expected_keys = submenu_expected_keys
    new_request_body = {
        "title": "Submenu changed",
        "description": "Submenu description changed"
    }
    expected_values = new_request_body | {"dishes_count": 0,
                                          "id": last_inserted_submenu_id}
    response = client.patch(f"/menus/{last_inserted_menu_id}"
                            f"/submenus/{last_inserted_submenu_id}",
                            json=new_request_body)
    assert response.status_code == status.HTTP_200_OK
    check_json_keys(response.json(), expected_keys)
    check_json_values(response.json(), expected_values)


def test_update_submenu_incorrect_body():
    expected_keys = expected_keys_422
    request_body = {"incorrect_key1": 1, "incorrect_key2": 2}
    response = client.patch(f"/menus/{last_inserted_menu_id}"
                            f"/submenus/{last_inserted_submenu_id}",
                            json=request_body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    check_json_keys(response.json(), expected_keys)


def test_update_submenu_404():
    expected_keys = expected_keys_404
    expected_values = submenu_expected_values_404
    new_request_body = {
        "title": "Submenu changed",
        "description": "Submenu description changed"
    }
    response = client.patch(f"/menus/{last_inserted_menu_id}"
                            f"/submenus/{uuid.uuid4()}",
                            json=new_request_body)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    check_json_keys(response.json(), expected_keys)
    check_json_values(response.json(), expected_values)


def test_delete_submenu():
    expected_keys = ["status", "message"]
    expected_values = {"status": True,
                       "message": "The submenu has been deleted"}
    response = client.delete(f"/menus/{last_inserted_menu_id}"
                             f"/submenus/{last_inserted_submenu_id}")
    assert response.status_code == status.HTTP_200_OK
    check_json_keys(response.json(), expected_keys)
    check_json_values(response.json(), expected_values)
    response = client.get(f"/menus/{last_inserted_menu_id}/submenus")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_delete_submenu_404():
    expected_keys = expected_keys_404
    expected_values = submenu_expected_values_404
    response = client.delete(f"/menus/{last_inserted_menu_id}"
                             f"/submenus/{last_inserted_submenu_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    check_json_keys(response.json(), expected_keys)
    check_json_values(response.json(), expected_values)
    client.delete(f"/menus/{last_inserted_menu_id}")
