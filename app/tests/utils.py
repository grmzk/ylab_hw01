def check_json_keys(response_json: dict, expected_keys: list):
    assert list(response_json.keys()) == expected_keys, (
        f"Expected json keys {expected_keys} but got {response_json.keys()}"
    )


def check_json_values(response_json: dict, expected_values: dict):
    for key, value in expected_values.items():
        assert response_json.get(key) == value, (
            f"Expected <{key}: {value}> "
            f"but got <{key}: {response_json.get(key)}> in json response"
        )
