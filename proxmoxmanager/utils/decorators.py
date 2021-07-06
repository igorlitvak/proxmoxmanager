from typing import Any, Union, Tuple, Sequence


def return_default_on_exception(default_value: Any = None,
                                catch_errors: Union[Exception, Tuple[Exception]] = Exception,
                                catch_with_args: Sequence = None):
    """
    Custom decorator that catches exceptions from function and returns some default value
    :param default_value: Any value to return if exception was caught (None by default)
    :param catch_errors: Types of errors to be caught (any exception by default)
    :param catch_with_args: Only catch exception if it contains these args
    :return: Normal function return if no exceptions were caught, default_value otherwise
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except catch_errors as e:
                if catch_with_args is None or e.args == tuple(catch_with_args):
                    return default_value
                else:
                    raise e

        return wrapper

    return decorator


def reraise_exception_on_exception(new_error: Exception,
                                   catch_errors: Union[Exception, Sequence[Exception]] = Exception,
                                   catch_with_args: Tuple = None):
    """
    Custom decorator that catches exceptions from function and reraises other exception
    :param new_error: Which exception must be raised
    :param catch_errors: Types of errors to be caught (any exception by default)
    :param catch_with_args: Only catch exception if it contains these args
    :return: Normal function return if no exceptions were caught
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except catch_errors as e:
                if catch_with_args is None or e.args == tuple(catch_with_args):
                    raise new_error
                else:
                    raise e

        return wrapper

    return decorator
