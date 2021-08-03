## What is the difference between the several **methods**?

```Python
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
Paw.some_instancemethod(1, 2, a=3, b=4)
print()
paw.some_classmethod(1, 2, a=3, b=4)
print()
Paw.some_classmethod()
print()
Paw.some_classmethod(1, 2, a=3, b=4)
print()
paw.some_staticmethod(1, 2, a=3, b=4)
print()
Paw.some_staticmethod()
print()
Paw.some_staticmethod(1, 2, a=3, b=4)
```

Gives the following outout:

```Python
 % python3 cat_paw.py
self: <__main__.Paw object at 0x7fc7d4f705b0>
args: (1, 2)
kwargs: {'a': 3, 'b': 4}

self: 1
args: (2,)
kwargs: {'a': 3, 'b': 4}

cls: <class '__main__.Paw'>
args: (1, 2)
kwargs: {'a': 3, 'b': 4}

cls: <class '__main__.Paw'>
args: ()
kwargs: {}

cls: <class '__main__.Paw'>
args: (1, 2)
kwargs: {'a': 3, 'b': 4}

args: (1, 2)
kwargs: {'a': 3, 'b': 4}

args: ()
kwargs: {}

args: (1, 2)
kwargs: {'a': 3, 'b': 4}
```
