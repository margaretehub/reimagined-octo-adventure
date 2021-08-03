import pprint


class Paw(object):
    def some_instancemethod(self, *args, **kwargs):
        print("self: %r" % self)
        print("args: %s" % pprint.pformat(args))
        print("kwargs: %s" % pprint.pformat(kwargs))

    @classmethod
    def some_classmethod(cls, *args, **kwargs):
        print("cls: %r" % cls)
        print("args: %s" % pprint.pformat(args))
        print("kwargs: %s" % pprint.pformat(kwargs))

    @staticmethod
    def some_staticmethod(*args, **kwargs):
        print("args: %s" % pprint.pformat(args))
        print("kwargs: %s" % pprint.pformat(kwargs))


paw = Paw()

paw.some_instancemethod(1, 2, a=3, b=4)
print()
# The instance method is the standard, it needs no decorator to be used.
# The first argument has to be the object that is created from the class.
# The method is used on the object-instance.
Paw.some_instancemethod(1, 2, a=3, b=4)
print()
# If you try to call the method directly on the class without instancing an object
# the first argument will be used instead of the self, the object-instance
# !this could lead to problems and it's dangerous!
paw.some_classmethod(1, 2, a=3, b=4)
print()
# The class-method can be used like a instance-method with an object.
Paw.some_classmethod()
print()
# But the speciality of the class-method is that you
Paw.some_classmethod(1, 2, a=3, b=4)
print()
paw.some_staticmethod(1, 2, a=3, b=4)
print()
# A static method doesn't receive any reference argument whether
# it is called by an instance of a class or by the class itself.
Paw.some_staticmethod()
print()
Paw.some_staticmethod(1, 2, a=3, b=4)
