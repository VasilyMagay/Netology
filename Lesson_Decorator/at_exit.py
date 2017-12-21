import atexit

@atexit.register
def my_fn():
    print('Bye Bye')


print('Hello')

