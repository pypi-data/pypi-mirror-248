import sys
from importlib import import_module

from property_based_testing.discovery.parse_test_suite import parse_test_suite
from property_based_testing.internal import run_test_suite
from property_based_testing.test_result import PropertyTestResult, Failure


def format_result(result: PropertyTestResult) -> str:
    if isinstance(result, Failure):
        return 'F'
    return '.'


def main(module_name: str) -> None:
    print(run_test_suite(parse_test_suite(import_module(module_name))))


if __name__ == '__main__':
    main(sys.argv[1])
