from inspect import getmembers, isfunction
from types import ModuleType
from typing import Any, TypeGuard, Callable

from property_based_testing.internal import FullyInjectedPropertyTest


def parse_test_suite(module: ModuleType) -> list[FullyInjectedPropertyTest]:
    return [
        property_test
        for name, property_test in getmembers(module)
        if is_property_test((name, property_test))
    ]


def is_property_test(module_member: tuple[str, Any]) -> TypeGuard[tuple[str, Callable[..., Any]]]:
    name, value = module_member
    return isfunction(value) and name.startswith('property_test')
