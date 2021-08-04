## Dataclasses in python

The python module [**dataclasses**](https://docs.python.org/3/library/dataclasses.html) goes as a decorator.

This module is a release in 2018. It has a short syntax to initialise a class particularly with property values:

```python
from dataclasses import dataclass


# The decorator:
@dataclass
class CatToy:
    """ Serialization informations of Cat Toys"""
    toy_name: str
    # <variable name> : <type>
    # This is the short way to declare class propertys
    quantity : int
    # declarations with default values can't be before required property
    # further down I will show the implicit built __init__ method, that will
    # make this determination clear
    description : str = 'description is missing'


```

The decorator implements automatically at least the *__\_\_init\_\_()__*, an *__\_\_repr\_\_()__* and an *__\_\_eq\_\_()__* methode.

```python

# This would be the equivalent __init__(), __repr__() and __eq__() methods:

class CatToyVerbose:
    def __init__(self, toy_name: str, quantity: int, description: str = 'description is missing'):
        self.toy_name = toy_name
        self.quantity = quantity
        self. description = description

    def __repr__(self):
        return str(self.__class__.__name__) + "(" +"', ".join([key+"='"+str(self.__dict__[key]) for key in self.__dict__])+"')"

    def __eq__(self, other):
        if self.__class__ is not other.__class__:
            return NotImplemented    
        return self.__dict__ == other.__dict__      
 ```

The \_\_repr\_\_ method returns an string that can be used to instance the class. It is callable with the [**repr(object)**](https://docs.python.org/3/library/functions.html#repr) method and in case it's possible returnable with [**eval(expression[, globals[, locals]])**](https://docs.python.org/3/library/functions.html#eval)  
