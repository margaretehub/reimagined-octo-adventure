## The python FastAPI framework

Within a few steps it's possible to create an API that is controlled by the **URL** and to work with the information in JSON format.

Also included in the framework is a automatic API-documentation:  */docs*

![docs FastAPI](./pictures/flask.png)

And it's also possible to write the API as an [__asynchronous__ application](./async_python.md).

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
2. Data validation with pydantic:

[Pydantic ](./pydantic.md) is a smart python module included in FastAPI, with the help of it data validation and serialization gets very easy and safe.

## Starting with the initialisation of a document in MongoDB with the **POST** command of FastAPI:

Commands of RESTful service like **GET**, **POST**, **PUT**, **PATCH**, **DELETE**, **HEAD**, **OPTIONS**, **CONNECT** and **TRACE** can be used in FastAPI:

In my code example I use the POST, PUT, GET and DELETE:

```python
...

@app.post("/", response_description="Add new cat", response_model=CatModel)
async def create_cat(cat: CatModel = Body(...)):
    cat = jsonable_encoder(cat)
    new_cat = await db["cats"].insert_one(cat)
    created_cat = await db["cats"].find_one({"_id": new_cat.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_cat)


@app.get("/", response_description="List all cats", response_model=List[CatModel])
async def list_cats():
    cats = await db["cats"].find().to_list(1000)
    return cats


@app.get("/{id}", response_description="Get a single cat", response_model=CatModel)
async def show_cat(id: str):
    if (cat := await db["cats"].find_one({"_id": id})) is not None:
        return cat

    raise HTTPException(status_code=404, detail=f"cat {id} not found")


@app.put("/{id}", response_description="Update a cat", response_model=CatModel)
async def update_cat(id: str, cat: UpdateCatModel = Body(...)):
    cat = {k: v for k, v in cat.dict().items() if v is not None}

    if len(cat) >= 1:
        update_result = await db["cats"].update_one({"_id": id}, {"$set": cat})

        if update_result.modified_count == 1:
            if (updated_cat := await db["cats"].find_one({"_id": id})) is not None:
                return updated_cat

    if (existing_cat := await db["cats"].find_one({"_id": id})) is not None:
        return existing_cat

    raise HTTPException(status_code=404, detail=f"cat {id} not found")


@app.delete("/{id}", response_description="Delete a cat")
async def delete_cat(id: str):
    delete_result = await db["cats"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"cat {id} not found")
```

All this commands are set up as decorators that decorate an async function with the syntax:
```python
@app.<rest_command>(<reference>, <config> ...)
```


##  The POST command
