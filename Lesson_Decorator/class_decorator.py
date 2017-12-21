def my_cls_decorator(cls):
    cls.Attribute = 123
    return cls


@my_cls_decorator
class MyCLS:
    pass


print(MyCLS.Attribute)
