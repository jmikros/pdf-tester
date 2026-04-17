from typing import Callable

# Global registry: (test_name_lower, description, function)
TESTS: list[tuple[str, str, Callable]] = []


def register_test(name: str, description: str):
    """Decorator to register a test"""
    def decorator(func: Callable):
        TESTS.append((name.lower(), description, func))
        return func
    return decorator


def get_all_test_names() -> list[str]:
    return [name for name, _, _ in TESTS]


def get_test_func(test_name: str) -> tuple[str, Callable] | None:
    """Find test by name (supports partial match)"""
    test_name = test_name.lower().strip()
    for name, _, func in TESTS:
        if test_name == name or test_name in name:
            return name, func
    return None