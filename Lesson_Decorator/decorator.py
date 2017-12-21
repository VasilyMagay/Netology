def print_decorator(fn):
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        print(result)

    return wrapper


def print_decorator_with_param(prefix, print_result=True):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            result = fn(*args, **kwargs)
            if print_result:
                print(prefix, result)

        return wrapper
    return decorator


# @print_decorator
# def my_function(a, b):
#     return (a + b) * 2

@print_decorator_with_param('Result:')
def my_function(a, b):
    return (a + b) * 2


my_function(1, 2)

