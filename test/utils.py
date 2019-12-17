def get_as_list(dict_object, key):
    value = dict_object.get(key)
    return value if value is not None else []


__all__ = ["get_as_list"]
