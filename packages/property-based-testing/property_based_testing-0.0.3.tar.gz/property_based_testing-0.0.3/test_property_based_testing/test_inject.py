from property_based_testing.api import inject
from property_based_testing.internal import FullyInjectedPropertyTest, run_test_suite
from property_based_testing.test_result import Failure, Success, PropertyTestResult
from test_property_based_testing.code_to_test_with import square, broken_square


def assert_is_failure(test_result: PropertyTestResult) -> None:
    assert isinstance(test_result, Failure)


def run_property_test_using_suite_runner(
    property_test: FullyInjectedPropertyTest,
    iterations: int = 1,
) -> PropertyTestResult:
    return next(iter(
        run_test_suite(
            [property_test],
            iterations=iterations,
        )
    ))


def test_run_property_based_test_runs_successful_tests_without_arguments() -> None:
    def property_test_that_1_squared_is_one() -> None:
        assert square(1) == 1

    assert run_property_test_using_suite_runner(property_test_that_1_squared_is_one) == Success()


def test_run_property_based_test_runs_unsuccessful_tests_without_arguments() -> None:
    def property_test_that_1_squared_is_19() -> None:
        assert square(1) == 19

    assert_is_failure(run_property_test_using_suite_runner(property_test_that_1_squared_is_19))


def test_inject_actually_injects_arguments() -> None:
    def positive_integer() -> int:
        return 3

    @inject(positive_integer)
    def property_test_squares_are_nonnegative(a: int) -> None:
        assert square(a) >= 0

    assert run_property_test_using_suite_runner(property_test_squares_are_nonnegative) == Success()


def test_run_property_test_using_suite_runner_does_multiple_iterations() -> None:
    integers_to_return = [3, 2, 2]

    def positive_integer() -> int:
        return integers_to_return.pop()

    @inject(positive_integer)
    def property_test_all_squares_are_4(a: int) -> None:
        assert square(a) == 4

    test_result = run_property_test_using_suite_runner(
        property_test=property_test_all_squares_are_4,
        iterations=3,
    )
    assert_is_failure(test_result)


def test_failing_test_propagate_custom_messages() -> None:
    def negative_integer() -> int:
        return -30

    custom_failure_message = "The square was not positive"

    @inject(negative_integer)
    def property_test_squares_are_positive(a: int) -> None:
        assert broken_square(a) > 0, custom_failure_message

    test_result = run_property_test_using_suite_runner(property_test=property_test_squares_are_positive)
    assert test_result == Failure(custom_failure_message)


def test_failing_test_without_message_does_not_propagate_message() -> None:
    def negative_integer() -> int:
        return -30

    @inject(negative_integer)
    def property_test_squares_are_positive(a: int) -> None:
        assert broken_square(a) > 0

    test_result = run_property_test_using_suite_runner(property_test=property_test_squares_are_positive)
    assert test_result == Failure(message=None)


def test_run_test_suite_for_empty_test_returns_empty_result_list() -> None:
    assert run_test_suite([]) == []


def test_run_test_suite_returns_all_results_in_order() -> None:
    def property_test_failing_test() -> None:
        assert False

    def property_test_passing_test() -> None:
        pass

    expected_result_types = [Failure, Success]
    actual_results = run_test_suite([property_test_failing_test, property_test_passing_test])

    for actual_result, expected_result_type in zip(actual_results, expected_result_types):
        assert isinstance(actual_result, expected_result_type)
