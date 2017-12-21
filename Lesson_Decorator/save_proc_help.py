from functools import wraps


def print_decorator(fn):
    @wraps(fn)  # Декаратор над обёрткой
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        print(result)
        return result
    return wrapper


@print_decorator
def my_function(a, b):
    '''
    My Great Doc
    :param a:
    :param b:
    :return:
    '''
    return (a + b) * 2


print(help(my_function))

