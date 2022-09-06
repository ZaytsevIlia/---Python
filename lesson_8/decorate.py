import sys
import traceback
from functools import wraps
import logging
import inspect


def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        calling_module = sys.argv[0].split('/')[-1].split('.')[0]
        var = func(*args, **kwargs)
        logger = logging.getLogger(calling_module)
        logger.debug(
            f'Функцию "{func.__name__}" вызвала функция "{inspect.stack()[1][3]}" '
            f'из модуля {func.__module__}.\n{" " * 35}'
            f'Параметры, которые были переданы {args, kwargs}'
        )
        return var

    return wrapper
