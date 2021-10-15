# -*- coding: utf-8 -*-
# -*- Python Version: 3.9 -*-

"""Set up the Function Decorators for the HBJSON->PHX logging"""

import logging
import inspect


def get_args_as_string(_func, args, kwargs):
    """Returns a function's arguments and keyword-arguments as a string."""

    # -- Get the kwarg defaults
    func_sig = inspect.signature(_func)
    kwarg_dict = {}
    for v in func_sig.parameters.values():
        if not v.default is inspect._empty:
            # -- Get only the kwargs
            kwarg_dict.update({v.name: v.default})

    # -- Update the kwarg dict with any passed kwargs
    for k, v in kwargs.items():
        kwarg_dict[k] = v

    kwargs_passed_to_func = [f"{k}={v}" for k, v in kwarg_dict.items()]
    args_passed_to_func = [repr(a) for a in args]
    str_args = ", ".join(args_passed_to_func + kwargs_passed_to_func)

    return str_args


def log_function_info(_func):
    """Decorator for Functions to log arguments and results"""

    logger = logging.getLogger("HBJSON")

    def wrapper(*args, **kwargs):
        str_args = get_args_as_string(_func, args, kwargs)

        try:
            value = _func(*args, **kwargs)
            logger.debug(f"{_func.__module__}.{_func.__name__}(\n  {str_args}\n  ) = {value}")
        except Exception as e:
            logger.debug(f"  ERROR: {_func.__name__}({str_args})")
            logger.debug(f"  ERROR: {e}")
            raise e

        return value

    return wrapper
