import uuid

from starlette import status

from conftest import client
from data import (dish_expected_keys, dish_expected_values_404,
                  dish_request_body1, expected_keys_404, expected_keys_422,
                  menu_request_body1, submenu_request_body1)
from utils import check_json_keys, check_json_values

last_inserted_menu_id: uuid = None
last_inserted_submenu_id: uuid = None
last_inserted_dish_id: uuid = None


def test_get_dishes_empty():
    global last_inserted_menu_id
    global last_inserted_submenu_id
    response = client.post("/menus", json=menu_request_body1)
    last_inserted_menu_id = response.json()["id"]
    response = client.post(f"/menus/{last_inserted_menu_id}/submenus",
                           json=submenu_request_body1)
    last_inserted_submenu_id = response.json()["id"]
    response = client.get(f"/menus/{last_inserted_menu_id}"
                          f"/submenus/{last_inserted_submenu_id}/dishes")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_create_dish():
    global last_inserted_submenu_id
    global last_inserted_dish_id
    expected_keys = dish_expected_keys
    expected_values = dish_request_body1
    response = client.post(f"/menus/{last_inserted_menu_id}"
                           f"/submenus/{last_inserted_submenu_id}/dishes",
                           json=dish_request_body1)
    assert response.status_code == status.HTTP_201_CREATED
    check_json_keys(response.json(), expected_keys)
    check_json_values(response.json(), expected_values)
    last_inserted_dish_id = response.json()["id"]


def test_create_dish_incorrect_body():
    expected_keys = expected_keys_422
    request_body = {"incorrect_key1": 1, "incorrect_key2": 2}
    response = client.post(f"/menus/{last_inserted_menu_id}"
                           f"/submenus/{last_inserted_submenu_id}/dishes",
                           json=request_body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    check_json_keys(response.json(), expected_keys)


def test_get_dishes_one_item():
    expected_keys = dish_expected_keys
    expected_values = dish_request_body1 | {"id": last_inserted_dish_id}
    response = client.get(f"/menus/{last_inserted_menu_id}"
                          f"/submenus/{last_inserted_submenu_id}/dishes")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1, (f"Expected 1 dish item, "
                                       f"but got {len(response)}")
    check_json_keys(response.json()[0], expected_keys)
    check_json_values(response.json()[0], expected_values)


def test_get_dish():
    expected_keys = dish_expected_keys
    expected_values = dish_request_body1 | {"id": last_inserted_dish_id}
    response = client.get(f"/menus/{last_inserted_menu_id}"
                          f"/submenus/{last_inserted_submenu_id}"
                          f"/dishes/{last_inserted_dish_id}")
    assert response.status_code == status.HTTP_200_OK
    check_json_keys(response.json(), expected_keys)
    check_json_values(response.json(), expected_values)


def test_get_dish_404():
    expected_keys = expected_keys_404
    expected_values = dish_expected_values_404
    response = client.get(f"/menus/{last_inserted_menu_id}"
                          f"/submenus/{last_inserted_submenu_id}"
                          f"/dishes/{uuid.uuid4()}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    check_json_keys(response.json(), expected_keys)
    check_json_values(response.json(), expected_values)


def test_update_dish():
    expected_keys = dish_expected_keys
    new_request_body = {
        "title": "Dish changed",
        "description": "Dish description changed",
        "price": "100.00"
    }
    expected_values = new_request_body | {"id": last_inserted_dish_id}
    response = client.patch(f"/menus/{last_inserted_menu_id}"
                            f"/submenus/{last_inserted_submenu_id}"
                            f"/dishes/{last_inserted_dish_id}",
                            json=new_request_body)
    assert response.status_code == status.HTTP_200_OK
    check_json_keys(response.json(), expected_keys)
    check_json_values(response.json(), expected_values)


def test_update_dish_incorrect_body():
    expected_keys = expected_keys_422
    request_body = {"incorrect_key1": 1, "incorrect_key2": 2}
    response = client.patch(f"/menus/{last_inserted_menu_id}"
                            f"/submenus/{last_inserted_submenu_id}"
                            f"/dishes/{last_inserted_dish_id}",
                            json=request_body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    check_json_keys(response.json(), expected_keys)


def test_update_dish_404():
    expected_keys = expected_keys_404
    expected_values = dish_expected_values_404
    new_request_body = {
        "title": "Dish changed",
        "description": "Dish description changed",
        "price": "100.00"
    }
    response = client.patch(f"/menus/{last_inserted_menu_id}"
                            f"/submenus/{last_inserted_submenu_id}"
                            f"/dishes/{uuid.uuid4()}",
                            json=new_request_body)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    check_json_keys(response.json(), expected_keys)
    check_json_values(response.json(), expected_values)


def test_delete_dish():
    expected_keys = ["status", "message"]
    expected_values = {"status": True,
                       "message": "The dish has been deleted"}
    response = client.delete(f"/menus/{last_inserted_menu_id}"
                             f"/submenus/{last_inserted_submenu_id}"
                             f"/dishes/{last_inserted_dish_id}")
    assert response.status_code == status.HTTP_200_OK
    check_json_keys(response.json(), expected_keys)
    check_json_values(response.json(), expected_values)
    response = client.get(f"/menus/{last_inserted_menu_id}"
                          f"/submenus/{last_inserted_submenu_id}/dishes")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_delete_dish_404():
    expected_keys = expected_keys_404
    expected_values = dish_expected_values_404
    response = client.delete(f"/menus/{last_inserted_menu_id}"
                             f"/submenus/{last_inserted_submenu_id}"
                             f"/dishes/{last_inserted_dish_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    check_json_keys(response.json(), expected_keys)
    check_json_values(response.json(), expected_values)
    client.delete(f"/menus/{last_inserted_menu_id}")
