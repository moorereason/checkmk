# -*- coding: utf-8 -*-
r"""
Test Check API
==============

Goal of the script
"""

import pytest

import cmk_base.check_api as check_api


@check_api.get_parsed_item_data
def check_foo(item, params, parsed_item_data):
    return 2, "bar"


def test_get_parsed_item_data():
    params = {}
    parsed = {1: "one", 3: {}, 4: [], 5: ""}
    info = [[1, "one"], [2, "two"]]
    assert check_foo(1, params, parsed) == (2, "bar")
    assert check_foo(2, params, parsed) is None
    assert check_foo(3, params, parsed) is None
    assert check_foo(4, params, parsed) is None
    assert check_foo(5, params, parsed) is None
    assert check_foo(1, params, info) == (3, "Wrong usage of decorator function 'get_parsed_item_data': parsed is not a dict")
    assert check_foo.__name__ == "check_foo"


def test_validate_filter():
    assert check_api.validate_filter(sum)((1, 4)) == 5

    with pytest.raises(ValueError):
        check_api.validate_filter("nothing")

    assert check_api.validate_filter(None)(1, 4) == 1


@pytest.mark.parametrize("parsed, result", [
    (None, None),
    ([], None),
    ({}, None),
    ([["enabled"]], [(None, {})]),
    ({
        "first": "enabled"
    }, [(None, {})]),
])
def test_discover_single(parsed, result):
    assert check_api.discover_single(parsed) == result


@pytest.mark.parametrize("parsed, selector, result", [
    ({}, lambda x: x, None),
    ({
        "one": None,
        "two": None,
    }, None, [("one", {}), ("two", {})]),
    ({
        "one": None,
        "two": None,
    }, lambda k, v: k, [("one", {}), ("two", {})]),
    ({
        "one": None,
        "two": None,
    }, lambda k, v: k.startswith("o"), [("one", {})]),
    ({
        "one": None,
        "two": None,
    }, lambda k, v: k == "one", [("one", {})]),
    ({
        "one": "enabled",
        "two": {
            "load": 10,
            "max": 50
        },
        "three": ["load", "capacity"],
    }, lambda k, values: "load" in values if isinstance(values, dict) else False, [("two", {})]),
    ({
        "one": "enabled",
        "two": {
            "load": 10,
            "max": 50,
            "Innodb_data_read": True
        },
    }, lambda k, values: "Innodb_data_read" in values, [("two", {})]),
    ({
        "one": "enabled",
        "two": {
            "load": 10,
            "Innodb_data_read": True
        },
    }, lambda key, values: all(val in values for val in ["load", "max"]), None),
    ({
        "one": [1],
        "two": [2],
        "three": [3],
        "four": (),
        "five": [],
    }, lambda k, value: len(value) > 0, [
        ("one", {}),
        ("two", {}),
        ("three", {}),
    ]),
    ([['one', 5, 3], ['two', 0, 0], ['three', 2, 8]], lambda line: line[0], [
        ("one", {}),
        ("two", {}),
        ("three", {}),
    ]),
    ([['one', 5, 3], ['two', 0, 0], ['three', 2, 8]],
     lambda line: line[0].upper() if line[1] > 0 else False, [
         ("ONE", {}),
         ("THREE", {}),
     ]),
])
def test_discover_inputs_and_filters(parsed, selector, result):
    items = list(check_api.discover(selector)(parsed))
    for item in items:
        assert item in result

    if result is not None:
        assert len(items) == len(result)
    else:
        assert items == []


def test_discover_decorator_key_match():
    @check_api.discover
    def selector(key, value):
        return key == "hello"

    assert list(selector({"hola": "es", "hello": "en"})) == [("hello", {})]


def test_discover_decorator_with_params():
    @check_api.discover(default_params="empty")
    def selector2(entry):
        return "hello" in entry

    assert list(selector2([["hello", "world"], ["hola", "mundo"]])) == [("hello", "empty")]


def test_discover_decorator_returned_name():
    @check_api.discover
    def inventory_thecheck(key, value):
        required_entries = ["used", "ready"]
        if all(data in value for data in required_entries):
            return key.upper()

    data = {
        'host': [['mysql', 10, 10], ['home', 5, 8]],
        'house': [['performance_schema', 5, 7], ['test', 1, 5]],
        'try': ['used', 'ready', 'total'],
    }

    assert list(inventory_thecheck(data)) == [('TRY', {})]


def test_discover_decorator_with_nested_entries():
    @check_api.discover
    def nested_discovery(instance, values):
        for dbname, used, avail in values:
            if dbname not in ["information_schema", "mysql", "performance_schema"] \
               and used != 'NULL' and avail != 'NULL':
                yield "%s:%s" % (instance, dbname)

    data = {
        'host': [['mysql', 10, 10], ['home', 5, 8]],
        'house': [['performance_schema', 5, 7], ['test', 1, 5]]
    }

    assert sorted(nested_discovery(data)) == [
        ("host:home", {}),
        ("house:test", {}),
    ]


@pytest.mark.parametrize("parsed, selector, error", [
    ({
        "one": None,
        "two": None,
    }, lambda k: k, (TypeError, r"takes exactly 1 argument \(2 given\)")),
    (None, lambda k, v: k.startswith("o"), (ValueError, "type 'NoneType'")),
    (list(range(5)), lambda k, v: v == k, (TypeError, r"takes exactly 2 arguments \(1 given\)")),
])
def test_discover_exceptions(parsed, selector, error):
    with pytest.raises(error[0], match=error[1]):
        next(check_api.discover(selector)(parsed))