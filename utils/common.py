from functools import wraps


def stack(debug=False):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            if debug:
                print(function.__name__)
            return function(*args, **kwargs)

        return wrapper

    return decorator
