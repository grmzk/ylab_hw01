menu_expected_keys = ["id", "title", "description",
                      "submenus_count", "dishes_count"]

menu_request_body1 = {
    "title": "Menu 1",
    "description": "Menu description 1"
}
menu_request_body2 = {
    "title": "Menu 2",
    "description": "Menu description 2"
}
menu_request_body3 = {
    "title": "Menu 3",
    "description": "Menu description 3"
}

submenu_expected_keys = ["id", "title", "description", "dishes_count"]

submenu_request_body1 = {
    "title": "Submenu 1",
    "description": "Submenu description 1"
}
submenu_request_body2 = {
    "title": "Submenu 2",
    "description": "Submenu description 2"
}
submenu_request_body3 = {
    "title": "Submenu 3",
    "description": "Submenu description 3"
}

dish_expected_keys = ["id", "title", "description", "price"]

dish_request_body1 = {
    "title": "Dish 1",
    "description": "Dish description 1",
    "price": "1.50"
}
dish_request_body2 = {
    "title": "Dish 2",
    "description": "Dish description 2",
    "price": "2.25"
}
dish_request_body3 = {
    "title": "Dish 3",
    "description": "Dish description 3",
    "price": "3.00"
}

expected_keys_404 = ["detail"]
menu_expected_values_404 = {"detail": "menu not found"}
submenu_expected_values_404 = {"detail": "submenu not found"}
dish_expected_values_404 = {"detail": "dish not found"}

expected_keys_422 = ["detail"]
