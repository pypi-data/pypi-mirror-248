from typing import Callable

from property_based_testing.dependency import Dependency, Dependencies


def inject(
    dependency_generator: Callable[[], Dependency],
) -> Callable[[Callable[[Dependency, *Dependencies], None]], Callable[[*Dependencies], None]]:
    def decorator(test: Callable[[Dependency, *Dependencies], None]) -> Callable[[*Dependencies], None]:
        def curried_test(*remaining_dependencies: *Dependencies) -> None:
            test(dependency_generator(), *remaining_dependencies)
        return curried_test
    return decorator
