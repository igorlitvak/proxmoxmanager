from typing import Any, Union, Tuple, Sequence, Dict


def return_default_on_exception(default_value: Any = None,
                                catch_errors: Union[Exception, Tuple[Exception]] = Exception,
                                with_args: Sequence = None,
                                with_fields: Dict[str, Any] = None):
    """
    ### DEVELOPMENT OF THIS DECORATOR WAS ABANDONED AND IT SHOULDN'T BE USED IN CURRENT FORM ###
    Custom decorator that catches exceptions from function and returns some default value
    :param default_value: Any value to return if exception was caught (None by default)
    :param catch_errors: Types of errors to be caught (any exception by default)
    :param with_args: Only catch exception if it contains these exact args
    :param with_fields: Only catch exception if it contains these fields
    :return: Normal function return if no exceptions were caught, default_value otherwise
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except catch_errors as e:
                if (with_args is None or e.args == tuple(with_args)) and (
                        with_fields is None or all(i in vars(e).items() for i in with_fields.items())):
                    return default_value
                else:
                    raise e

        return wrapper

    return decorator


def reraise_exception_on_exception(new_error: Exception,
                                   catch_errors: Union[Exception, Sequence[Exception]] = Exception,
                                   with_args: Sequence = None,
                                   with_fields: Dict[str, Any] = None):
    """
    ### DEVELOPMENT OF THIS DECORATOR WAS ABANDONED AND IT SHOULDN'T BE USED IN CURRENT FORM ###
    Custom decorator that catches exceptions from function and reraises other exception
    :param new_error: Which exception must be raised
    :param catch_errors: Types of errors to be caught (any exception by default)
    :param with_args: Only catch exception if it contains these exact args
    :param with_fields: Only catch exception if it contains these fields
    :return: Normal function return if no exceptions were caught
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except catch_errors as e:
                if (with_args is None or e.args == tuple(with_args)) and (
                        with_fields is None or all(i in vars(e).items() for i in with_fields.items())):
                    raise new_error
                else:
                    raise e

        return wrapper

    return decorator
