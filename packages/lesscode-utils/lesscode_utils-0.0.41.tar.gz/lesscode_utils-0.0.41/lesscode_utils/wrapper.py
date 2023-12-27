import functools
import traceback


def retry(num=3, check_func=None):
    def _retry(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for i in range(num):
                try:
                    result = func(*args, **kwargs)
                    if check_func is not None:
                        if check_func(result):
                            break
                except Exception as e:
                    traceback.print_exc()
                    if i == num - 1:
                        raise e
            return result

        return wrapper

    return _retry
