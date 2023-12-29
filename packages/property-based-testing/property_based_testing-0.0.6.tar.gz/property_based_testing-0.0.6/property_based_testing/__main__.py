import sys
from importlib import import_module

from property_based_testing.discovery.parse_test_suite import parse_test_suite
from property_based_testing.internal import run_test_suite


def main(module_name: str) -> None:
    print(run_test_suite(parse_test_suite(import_module(module_name))))


if __name__ == '__main__':
    main(sys.argv[1])
