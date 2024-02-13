import json
import os
from functools import wraps
from uuid import UUID

from pydantic import BaseModel
from redis import StrictRedis
from starlette.responses import JSONResponse

from database import redis_cache
from menus.schemas import DishReadSchema  # noqa
from menus.schemas import MenuReadSchema  # noqa
from menus.schemas import SubmenuReadSchema  # noqa

# RESPONSE_CACHER_DISABLE - environment variable, may be `0` for cache enable
# or `1` for cache disable
RESPONSE_CACHER_DISABLE = int(os.getenv("RESPONSE_CACHER_DISABLE", default=0))


class ResponseCacher:
    def __init__(self, cache: StrictRedis):
        self.cache = cache

    @staticmethod
    def get_key_str(**kwargs):
        key_dict = dict()
        for key, value in kwargs.items():
            if isinstance(value, UUID):
                key_dict[key] = str(value)
        return json.dumps(key_dict)

    def add(self, endpoint_name: str, response, **kwargs):
        name = endpoint_name
        key = self.get_key_str(**kwargs)
        is_list = 0
        data = None
        item_class = type(response)
        if isinstance(response, list):
            is_list = 1
            if len(response):
                item_class = type(response[0])
            else:
                item_class = type(None)
            data = [item.model_dump_json() for item in response]
        elif issubclass(item_class, BaseModel):
            data = response.model_dump_json()
        elif issubclass(item_class, JSONResponse):
            data = {
                "status_code": response.status_code,
                "content": json.loads(response.body)
            }
        else:
            raise ValueError(f"Response class <{item_class.__name__}> "
                             "is not supported!")
        data_dict = {
            "is_list": is_list,
            "item_class_name": item_class.__name__,
            "data": data
        }
        self.cache.hset(name=name, key=key, value=json.dumps(data_dict))

    def get(self, endpoint_name: str, **kwargs):
        name = endpoint_name
        key = self.get_key_str(**kwargs)
        data_dict = json.loads(self.cache.hget(name=name, key=key))
        is_list = data_dict["is_list"]
        item_class_name = data_dict["item_class_name"]
        data = data_dict["data"]
        if item_class_name == "NoneType":
            return data
        item_class = eval(item_class_name)
        if is_list:
            return (
                [item_class.model_validate_json(item) for item in data]
            )
        if issubclass(item_class, BaseModel):
            return item_class.model_validate_json(data)
        if issubclass(item_class, JSONResponse):
            return JSONResponse(**data)
        raise ValueError(f"Response class <{item_class.__name__}> "
                         "is not supported!")

    def exists(self, endpoint_name: str, **kwargs):
        name = endpoint_name
        key = self.get_key_str(**kwargs)
        return self.cache.hexists(name=name, key=key)

    def delete(self, endpoint_name: str, **kwargs):
        name = endpoint_name
        if not kwargs:
            self.cache.delete(name)
            return
        key = self.get_key_str(**kwargs)
        if name.endswith("+"):
            name = name[:-1]
            for hg_key in self.cache.hgetall(name=name).keys():
                if hg_key.startswith(key[:-1]):
                    hg_keys = [hg_key]
                    self.cache.hdel(name, *hg_keys)
                    return
        keys = [key]
        self.cache.hdel(name, *keys)


response_cacher = ResponseCacher(redis_cache)


def cache_add(endpoint):
    """Decorator for adding endpoint's response data to cache.
    Used without arguments."""
    @wraps(endpoint)
    def wrapper(*args, **kwargs):
        print(f"RESPONSE_CACHER_DISABLE = {RESPONSE_CACHER_DISABLE}")
        if not RESPONSE_CACHER_DISABLE:
            if response_cacher.exists(endpoint.__name__, **kwargs):
                return response_cacher.get(endpoint.__name__, **kwargs)
        response = endpoint(*args, **kwargs)
        if not RESPONSE_CACHER_DISABLE:
            response_cacher.add(endpoint.__name__, response, **kwargs)
        return response
    return wrapper


def cache_delete(endpoints: dict[str, list[str]]):
    """Decorator for deleting endpoint's response data from cache.
    Required argument `endpoints` is dictionary with endpoint_name (type: str)
    as key and list of items ids as value.
    Example:
        @cache_delete({"get_menus": [], "get_menu": ["menu_id"]})
    If endpoint_name in key ends with "+" then deleting all items from cache
    which key names begins with items ids from dictionary key's list.
    Example:
        @cache_delete({"get_dish+": ["menu_id"]})"""
    def inner_func(endpoint):
        @wraps(endpoint)
        def wrapper(*args, **kwargs):
            if not RESPONSE_CACHER_DISABLE:
                for endpoint_name, keys in endpoints.items():
                    key_dict = dict()
                    for key in keys:
                        key_dict[key] = kwargs[key]
                    response_cacher.delete(endpoint_name, **key_dict)
            return endpoint(*args, **kwargs)
        return wrapper
    return inner_func
