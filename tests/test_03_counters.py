import uuid

from starlette import status

from conftest import client
from data import (dish_request_body1, dish_request_body2, dish_request_body3,
                  menu_request_body1, menu_request_body2, menu_request_body3,
                  submenu_request_body1, submenu_request_body2,
                  submenu_request_body3)

menu_id1: uuid = None
menu_id2: uuid = None
menu_id3: uuid = None
submenu_id1: uuid = None
submenu_id2: uuid = None
submenu_id3: uuid = None
dish_id1: uuid = None
dish_id2: uuid = None
dish_id3: uuid = None


def test_menu_submenus_count_zero():
    global menu_id1, menu_id2, menu_id3
    response = client.post("/menus", json=menu_request_body1)
    menu_id1 = response.json()["id"]
    response = client.post("/menus", json=menu_request_body2)
    menu_id2 = response.json()["id"]
    response = client.post("/menus", json=menu_request_body3)
    menu_id3 = response.json()["id"]
    for menu_id in (menu_id1, menu_id2, menu_id3):
        response = client.get(f"/menus/{menu_id}")
        assert response.json()["submenus_count"] == 0


def test_menu_dishes_count_zero():
    for menu_id in (menu_id1, menu_id2, menu_id3):
        response = client.get(f"/menus/{menu_id}")
        assert response.json()["dishes_count"] == 0


def test_menu_submenus_count():
    global submenu_id1, submenu_id2, submenu_id3
    response = client.post(f"/menus/{menu_id1}/submenus",
                           json=submenu_request_body1)
    submenu_id1 = response.json()["id"]
    response = client.post(f"/menus/{menu_id1}/submenus",
                           json=submenu_request_body2)
    submenu_id2 = response.json()["id"]
    response = client.post(f"/menus/{menu_id2}/submenus",
                           json=submenu_request_body3)
    submenu_id3 = response.json()["id"]
    response = client.get(f"/menus/{menu_id1}")
    assert response.json()["submenus_count"] == 2
    response = client.get(f"/menus/{menu_id2}")
    assert response.json()["submenus_count"] == 1
    response = client.get(f"/menus/{menu_id3}")
    assert response.json()["submenus_count"] == 0


def test_menu_dishes_count():
    global dish_id1, dish_id2, dish_id3
    response = client.post(f"/menus/{menu_id1}/submenus/{submenu_id1}/dishes",
                           json=dish_request_body1)
    dish_id1 = response.json()["id"]
    response = client.post(f"/menus/{menu_id1}/submenus/{submenu_id1}/dishes",
                           json=dish_request_body2)
    dish_id2 = response.json()["id"]
    response = client.post(f"/menus/{menu_id1}/submenus/{submenu_id2}/dishes",
                           json=dish_request_body3)
    dish_id3 = response.json()["id"]
    response = client.get(f"/menus/{menu_id1}")
    assert response.json()["dishes_count"] == 3
    response = client.get(f"/menus/{menu_id2}")
    assert response.json()["dishes_count"] == 0
    response = client.get(f"/menus/{menu_id3}")
    assert response.json()["dishes_count"] == 0


def test_submenu_dishes_count():
    response = client.get(f"/menus/{menu_id1}/submenus/{submenu_id1}")
    assert response.json()["dishes_count"] == 2
    response = client.get(f"/menus/{menu_id1}/submenus/{submenu_id2}")
    assert response.json()["dishes_count"] == 1
    response = client.get(f"/menus/{menu_id2}/submenus/{submenu_id3}")
    assert response.json()["dishes_count"] == 0


def test_menu_submenus_count_after_submenu_delete():
    client.delete(f"/menus/{menu_id1}/submenus/{submenu_id1}")
    response = client.get(f"/menus/{menu_id1}")
    assert response.json()["submenus_count"] == 1
    response = client.get(f"/menus/{menu_id2}")
    assert response.json()["submenus_count"] == 1
    response = client.get(f"/menus/{menu_id3}")
    assert response.json()["submenus_count"] == 0


def test_menu_dishes_count_after_submenu_delete():
    response = client.get(f"/menus/{menu_id1}")
    assert response.json()["dishes_count"] == 1
    response = client.get(f"/menus/{menu_id2}")
    assert response.json()["dishes_count"] == 0
    response = client.get(f"/menus/{menu_id3}")
    assert response.json()["dishes_count"] == 0


def test_all_menu_delete():
    client.delete(f"/menus/{menu_id1}")
    client.delete(f"/menus/{menu_id2}")
    client.delete(f"/menus/{menu_id3}")
    response = client.get("/menus")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
