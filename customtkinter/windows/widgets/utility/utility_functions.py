from __future__ import annotations

from typing import Any, TypeVar

KT = TypeVar("KT")
VT = TypeVar("VT")


def pop_from_dict_by_set(dictionary: dict[KT, VT], valid_keys: set[KT]) -> dict[KT, VT]:
    """ remove and create new dict with key value pairs of dictionary, where key is in valid_keys """
    new_dictionary: dict[KT, VT] = {}

    for key in list(dictionary.keys()):
        if key in valid_keys:
            new_dictionary[key] = dictionary.pop(key)

    return new_dictionary


def check_kwargs_empty(kwargs_dict: dict[Any, Any], raise_error: bool =False) -> bool:
    """ returns True if kwargs are empty, False otherwise, raises error if not empty """

    if len(kwargs_dict) > 0:
        if raise_error:
            raise ValueError(f"{list(kwargs_dict.keys())} are not supported arguments. Look at the documentation for supported arguments.")
        else:
            return True
    else:
        return False
