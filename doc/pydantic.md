## The python pydantic module used inside FastAPI:

FastAPI uses the [**pydantic**](https://pydantic-docs.helpmanual.io) library to review and process the data. It's a quick, but easy-to-use package. To create a pydantic model to use it in FastAPI a self-created Class has to inherit the pydantic **BaseModel**:

```Python
from pydantic import BaseModel, Field
from typing import Optional, List

class CatModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    # It's something special going on with PyObjectId ... more later
    catname: str = Field(...)
    skill: str = Field(...)
    strength: float = Field(..., le=4.0)

```
The propertys of CatModel are surrounded with [__type annotations__](https://docs.python.org/3/library/typing.html#module-typing). Type annotations in python **are not effecting the compiler or runtime**, there will be no error caused of missmatching the annotations, maybe this could be missleading. Rather they are notes in the code for developers.

The syntax is:

```Python
# For variables:
<variablename>: <type>
# For functions:
def <functionname>(<parameter>) -> <type>:
# Type annotations are hints what type is required for the variable
# or what kind of return-type of a function is expected

```

## So what does pydantic?

Pydantic converts data in python format, in this case: It attempts to coerce it in the annotated type. There is also the possibility to mark the type of the model as __Optional__ or to provide default values. And it provides very detailed error messages:

This code:

```Python
from pydantic import BaseModel, Field, ValidationError
from typing import Optional, List
from BSON import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class CatModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    catname: str = Field(...)
    skill: str = Field(...)
    strength: float = Field(..., le=4.0)

try:
    cat = CatModel(catname='Waltraud', skill='Fight with Axes', strength='She can prevail')
    print(cat)
except ValidationError as e:
    print(e.json())
```

Comes to this output:

```Python

[
  {
    "loc": [
      "strength"
    ],
    "msg": "value is not a valid float",
    "type": "type_error.float"
  }
]

```

And now to the **PyObjectId** class:
The PyObjectId inherits from **BSONs ObjectId** let's take a closer look in it.

## [BSON's ObjectId](https://docs.mongodb.com/manual/reference/method/ObjectId/):

ObjectId is an extremely clever data type from the Mongo database. It not only guarantees unique IDs, but also saves the creation date, as a timestamp, in the same pass with in the ObjectId.

[Here](https://BSONspec.org/spec.html) is the specification of BSON in a pseudo-BFN syntax.
This element of the BSON document has a size of 12 byte.

The ObjectId also has a property the __timestamp__ that is reachable with the:

```Python
bson.objectid.ObjectId.generation_time
```

and also a __validation method__ that checks if the given string is a valid ObjectId or not:

```Python
bson.objectid.ObjectId.is_valid(str)
```
[Look](#so-what-does-pydantic) upwards in the code there in the PyObjectId this particular ObjectId-method is found inside the **validate-method**.


[\@classmethod](https://docs.python.org/3/library/functions.html#classmethod) is a decorator:
[The difference between classmethod and staticmethod:](./classmeth_vs_staticmeth.md)
The classmethod passes a **class object** instead of a **class instance** (explict: _self_)



## Creating an own pydantic data type:

There a few ways to create a own datatype. For the case of **ObjectId** it's really important, because there is no pythonic datatype like this.

A type that can be build, for that reason uses FastAPI at least three decorated methods:

```python
__get_validators__()
__modify_schema__()
validate()

```
Let's have again a deepeer look into the CatModel example:

```python

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
        # This will yield the proper validate methods

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)
        # This will be used to validate the value in the way we want it to be
        # It returns an object:
        # An ObjectId-object that will be stored as PyObjectId

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")
        # Here the field_schema-dict is updated to the type: 'string'


class CatModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    # The default factory is used in case no value is given
    # The PyObjectId inherits from ObjectId from pymongos bson that creates a
    # ObjectId by calling the class:
    #
    # >>> from bson import ObjectId
    # >>> ObjectId()
    # ObjectId('61095187da5556bd5cc9a4f7')
    #
    #
    catname: str = Field(...)
    # To declare a field as required, you may declare it using just an annotation,
    # or you may use an ellipsis (...) as the value
    skill: str = Field(...)
    strength: float = Field(..., le=4.0)
```
'...' is the literal for the special value _Ellipsis_ a build-in constant of python.
'A(s) non-used literal, you can use the ellipsis object.'
'So if you see yourself in the situation that you are developing a new tool or library and need a placeholder literal, remind yourself of the ellipsis object!' Quotes from Florian Daliz: [What is Python's Ellipsis Object?](https://florian-dahlitz.de/articles/what-is-pythons-ellipsis-object)

## The **Field(...)**
The Field()-instance allows to change settings for a several Field like:
It's like the little sister of the Config subclass, the Config subclass property applies for all fields in the class, but the Field() specifications just for the one field.
The first argument is the **default** value of the field, the **ellipsis** shows there that the field is required.
Instead of using default, **default_factory** can be used. The default_factory needs a callable element that returns a standard value for the field.
**alias** is the public name of the field. **description**, the description of the field uses if not declared, the docstring if possible of the annotation.
The **title** value is created with field_name.title(), if not declared in the Field()-instance.
**gt**, **ge**, **lt**, **le**, **multiple_of** are mathematical validations.
**min_items** and **max_items** are determinations for _list_ values.
**min_length** and **max_length** are determinations for _string_ values.




## The **Config**-sub-class of pydantics **BaseModel**:

```python
class Config:
      allow_population_by_field_name = True
      arbitrary_types_allowed = True
      json_encoders = {ObjectId: str}
      schema_extra = {
          "example": {
              "catname": "Kitty Lilly",
              "skill": "Drinks Seawater, Knows How To Deal With Hairballs",
              "strength": "13.0",
          }
      }
```
The Config class is a class in the class that inherits from BaseModel. In Config all of the Configuration-Data is saved, that regards the parsing. It's possible to decide the maximum or minimum length of a string, to strip the whitespaces, if it's allowed to assign extra attributes by initialisation.

```python
allow_mutation default:False
# Allows the reassigning of the the field or not
frozen default: True
# Is similar to allow_mutation=False when True, but additional it generates a __hash__() method for the model
# That makes it hashable
use_enum_values default: False
# If it's True than it uses the number assigned to the particular Enum to safe the value
fields type: dict
# Adds schema information for each field like this:
# fields = {
#           'auth_key': {
#               'env': 'my_auth_key',
#           },
#           'redis_dsn': {
#               'env': ['service_redis_dsn', 'redis_url']
#           }
#       }
validate_assignment default: False
#
allow_population_by_field_name default: False
# Access to population of a field by field-name and alias
error_msg_templates type: dict
# Allows to override the error message templates
arbitrary_types_allowed default: False
# In my example I am using the arbitrary_types_allowed configuration to allow CatModel to use
# the self-made Class PyObjectId  
orm_mode default: False
# Allows to retrieve data from object–relational mapping:
# When it's set on True Objects can be read out
# and mapped with the help of the Class that inherits the BaseModel
#
```

Object-relational mapping is a technic from software development within it can be achieved that objects out of a object-oriented language can be saved in a RDBMS. The software that is in connection with the database can work as if it is an object database. In python there is the class library [SQLALchemy](https://www.sqlalchemy.org)

```python
alias_generator type: callable
# Returns a alias for every field name
schema_extra type: dict
# Add as an example for the API documentation
json_loads type: function
# For decoding JSON
json_dumps type: function
# For encoding JSON
json_encoders type: dict
# For customised serialization like in this example:
#
#from datetime import datetime, timedelta
#from pydantic import BaseModel
#from pydantic.json import timedelta_isoformat
#
#
#class WithCustomEncoders(BaseModel):
#    dt: datetime
#    diff: timedelta
#
#    class Config:
#        json_encoders = {
#            datetime: lambda v: v.timestamp(),
#            timedelta: timedelta_isoformat,
#        }
#
underscore_attrs_are_private type: boolean
# Private attribute names must start with underscore to prevent conflicts with model fields:
# both _attr and __attr__ are supported
copy_on_model_validation default: True
# whether or not inherited models used as fields
# should be reconstructed (copied) on validation instead of being kept untouched

```

## Ways to initialise Model Config:

1. Config Options as **kwargs** in the model class:
  ```python
  ...
  class GoodModel(BaseModel, underscore_attrs_are_private=True):
    ...
```

2.  Using a inner class **Config**:
  My code example uses such a class.

3. Or if the decorator \@dataclass is used, giving the configuration into the **config parameter** of the decorator:

## Ways to set Configuration globally:
   Is to add **BaseModel** a inner Config class

```python
from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True


class MyClass:
    """A random class"""


class Model(BaseModel):
    x: MyClass

```
