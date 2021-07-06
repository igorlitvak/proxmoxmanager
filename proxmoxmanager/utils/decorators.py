from typing import Any, Sequence


def return_default_on_exception(default_value=None, catch_errors: Sequence[Exception] = (Exception,)):
    """
    Custom decorator that catches exceptions from function and returns some default value
    :param default_value: Any value to return if exception was caught (None by default)
    :param catch_errors: Types of errors to be caught (any exception by default)
    :return: Normal function return if no exceptions were caught, default_value otherwise
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except catch_errors:
                return default_value

        return wrapper

    return decorator


def reraise_exception_on_exception(new_error: Exception, catch_errors: Sequence[Exception] = (Exception,)):
    """
    Custom decorator that catches exceptions from function and reraises other exception
    :param new_error: Which exception must be raised
    :param catch_errors: Types of errors to be caught (any exception by default)
    :return: Normal function return if no exceptions were caught
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except catch_errors:
                raise new_error

        return wrapper

    return decorator
