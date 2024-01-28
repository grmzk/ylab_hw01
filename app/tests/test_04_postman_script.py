import uuid

from starlette import status

from conftest import client

target_menu_id: uuid = None
target_submenu_id: uuid = None
target_dish_id1: uuid = None
target_dish_id2: uuid = None


def test_create_menu():
    global target_menu_id
    request_body = {"title": "My menu 1",
                    "description": "My menu description 1"}
    response = client.post("/menus", json=request_body)
    assert response.status_code == status.HTTP_201_CREATED
    target_menu_id = response.json()["id"]


def test_create_submenu():
    global target_submenu_id
    request_body = {"title": "My submenu 1",
                    "description": "My submenu description 1"}
    response = client.post(f"/menus/{target_menu_id}/submenus",
                           json=request_body)
    assert response.status_code == status.HTTP_201_CREATED
    target_submenu_id = response.json()["id"]


def test_create_dish1():
    global target_dish_id1
    request_body = {"title": "My dish 2",
                    "description": "My dish description 2",
                    "price": "13.50"}
    response = client.post(f"/menus/{target_menu_id}"
                           f"/submenus/{target_submenu_id}/dishes",
                           json=request_body)
    assert response.status_code == status.HTTP_201_CREATED
    target_dish_id1 = response.json()["id"]


def test_create_dish2():
    global target_dish_id2
    request_body = {"title": "My dish 1",
                    "description": "My dish description 1",
                    "price": "12.50"}
    response = client.post(f"/menus/{target_menu_id}"
                           f"/submenus/{target_submenu_id}/dishes",
                           json=request_body)
    assert response.status_code == status.HTTP_201_CREATED
    target_dish_id2 = response.json()["id"]


def test_get_menu_1():
    global target_menu_id
    response = client.get(f"/menus/{target_menu_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == target_menu_id
    assert response.json()["submenus_count"] == 1
    assert response.json()["dishes_count"] == 2


def test_get_submenu():
    response = client.get(f"/menus/{target_menu_id}"
                          f"/submenus/{target_submenu_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == target_submenu_id
    assert response.json()["dishes_count"] == 2


def test_delete_submenu():
    response = client.delete(f"/menus/{target_menu_id}"
                             f"/submenus/{target_submenu_id}")
    assert response.status_code == status.HTTP_200_OK


def test_get_submenus():
    response = client.get(f"/menus/{target_menu_id}/submenus")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_get_dishes():
    response = client.get(f"/menus/{target_menu_id}"
                          f"/submenus/{target_submenu_id}/dishes")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_get_menu_2():
    response = client.get(f"/menus/{target_menu_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == target_menu_id
    assert response.json()["submenus_count"] == 0
    assert response.json()["dishes_count"] == 0


def test_delete_menu():
    response = client.delete(f"/menus/{target_menu_id}")
    assert response.status_code == status.HTTP_200_OK


def test_get_menus():
    response = client.get("/menus")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
