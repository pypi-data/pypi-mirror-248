from typing import Callable, NewType

from property_based_testing.make_property_test import make_property_test
from property_based_testing.test_result import Failure, Success, PropertyTestResult

FullyInjectedPropertyTest = Callable[[], None]


TestName = NewType('TestName', str)


def run_test_suite(
    test_suite: list[FullyInjectedPropertyTest],
    iterations: int = 1,
) -> dict[TestName, PropertyTestResult]:
    return {
        TestName(property_test.__name__): run_property_test(property_test, iterations=iterations)
        for property_test in test_suite
    }


def run_property_test(
    property_test: FullyInjectedPropertyTest,
    iterations: int = 1,
) -> PropertyTestResult:
    actual_property_test = make_property_test(property_test)
    for _ in range(iterations):
        test_result = actual_property_test()
        if isinstance(test_result, Failure):
            return test_result

    return Success()
