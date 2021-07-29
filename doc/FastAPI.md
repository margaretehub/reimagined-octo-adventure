## The python FastAPI framework

Within a few steps it's possible to create an API that is controlled by the **URL** and to work with the information in JSON format.

Also included in the framework is a automatic API-documentation:  */docs*

![docs FastAPI](./pictures/Screenshot)

And it's also possible to write the API as an __asynchronous__ application

## The idea of asynchrony in python:

Fast application need smart programming, in order to get for example a server application that can handle the needs of different parts of a program,  
different modules or functions that need to wait the results of each other,  
that's what asynchronous programming is for.

In python the syntax for it are the **coroutines** in the module **asyncio**:

**async** and **await**

__async__ marks the methods as asynchronous methods, __await__ is the checkpoint where one function can go to another.

The difference between **threads** and **coroutines** is: By using threads the operating system decides to switch to another task. Coroutines only switches when there is an "await".  

## Implementing a No-SQL database into FastAPI framework

(more soon..)
