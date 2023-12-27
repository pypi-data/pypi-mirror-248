#!/usr/bin/python
# encoding=utf-8

import json
import re
from typing import Any

from tep.keywords.impl.VarImpl import replace_var


def JSONImpl(json_str: str, expr: dict = None) -> dict:
    new_str = replace_var(json_str)
    if new_str:
        return json.loads(new_str)

    if expr:
        json_obj = json.loads(json_str)
        for json_path, value in expr.items():
            _assign(json_obj, json_path, value)
        return json_obj

    return json.loads(json_str)


def _jsonpath_to_dict_expr(jsonpath: str) -> str:
    """
    Input: $.store.book[0].title
    Output: '["store"]["book"][0]["title"]'
    """
    tokens = re.findall(r'\.(\w+)|\[(\d+)\]', jsonpath)
    expr = ''
    for token in tokens:
        if token[0]:
            expr += '["{}"]'.format(token[0])
        else:
            expr += '[{}]'.format(token[1])
    return expr


def _parse_dict_expr(expr: str) -> list:
    """
    Input: '["store"]["book"][0]["title"]'
    Output: ['store', 'book', 0, 'title']
    """
    tokens = re.findall(r'\["(.*?)"\]|\[(\d+)\]', expr)
    result = [int(index) if index.isdigit() else name for name, index in tokens]
    return result


def _nested_modify(json_obj: [dict, list], keys: list, value: Any, current_level: int = 0):
    if current_level == len(keys) - 1:
        json_obj[keys[current_level]] = value
    else:
        current_key = keys[current_level]
        # Nested string json {"id": 1, "param": "{\"page\": 1}"}
        if isinstance(json_obj[current_key], str):
            # str to json
            current_value = json.loads(json_obj[current_key])
            if isinstance(current_value, dict) or isinstance(current_value, list):
                nested_string_json_obj = current_value
                _nested_modify(nested_string_json_obj, keys[current_level + 1:], value)
                # json to str
                json_obj[current_key] = json.dumps(nested_string_json_obj, ensure_ascii=False)
        else:
            _nested_modify(json_obj[current_key], keys, value, current_level + 1)


def _assign(json_obj: [dict, list], json_path: str, value: Any):
    dict_expr = _jsonpath_to_dict_expr(json_path)
    keys = _parse_dict_expr(dict_expr)
    _nested_modify(json_obj, keys, value)
