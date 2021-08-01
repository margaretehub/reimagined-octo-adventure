## The python FastAPI framework

Within a few steps it's possible to create an API that is controlled by the **URL** and to work with the information in JSON format.

Also included in the framework is a automatic API-documentation:  */docs*

![docs FastAPI](./pictures/flask.png)

And it's also possible to write the API as an __asynchronous__ application

## The idea of asynchrony in python:

Fast application need smart programming, in order to get for example a server application that can handle the needs of different parts of a program, different modules or functions that need to wait the results of each other, that's what asynchronous programming is for.

In python the syntax for it are the **coroutines** in the module **asyncio**:

**async** and **await**

__async__ marks the methods as asynchronous methods, __await__ is the checkpoint where one function can go to another.

The difference between **threads** and **coroutines** is: By using threads the operating system decides to switch to another task. Coroutines only switches when there is an "await".  

## Implementing a MongoDB database into FastAPI framework

![Overview Catperson API](./pictures/cat_overview.png)

There are a few parts to take care of to write a MongoDB with a FastAPI framework.  
My first small [example API](./cat/app.py) is a initial attempt, a small modification of [this](https://github.com/mongodb-developer/mongodb-with-fastapi#readme) source code, I will go through the code step by step and illuminate and understand the individual components. 
1. Connection:

For the connection purpose it is using the [**motor**](https://motor.readthedocs.io/en/stable/) API:

```python
app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.catworld
```

The **MONGODB_URL** environment string is the connection string. It looks like this:

```
"mongodb+srv://<username>:<password>@<url>/<db>?retryWrites=true&w=majority"
```

But just to try it out, this string can be used:

```
"mongodb://localhost:270172"
```
