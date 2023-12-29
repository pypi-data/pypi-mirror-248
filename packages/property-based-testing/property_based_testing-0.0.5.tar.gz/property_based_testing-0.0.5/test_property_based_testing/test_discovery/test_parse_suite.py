import pytest

from property_based_testing.discovery.parse_test_suite import parse_test_suite
from test_property_based_testing.test_discovery import empty_test_suite, property_test_suite_with_one_test, \
    property_test_suite_with_one_non_test, property_test_suite_with_one_failing_test


def test_parsing_suite_without_tests_succeeds() -> None:
    assert parse_test_suite(empty_test_suite) == []


def test_parsing_suite_with_one_test_finds_one_test() -> None:
    assert len(parse_test_suite(property_test_suite_with_one_test)) == 1


def test_parsing_suite_only_sees_functions_starting_with_property_test() -> None:
    assert len(parse_test_suite(property_test_suite_with_one_non_test)) == 1


def test_parsing_suite_actually_returns_runnable_module_members() -> None:
    test_suite = parse_test_suite(property_test_suite_with_one_failing_test)
    property_test = next(iter(test_suite))

    with pytest.raises(AssertionError):
        property_test()
