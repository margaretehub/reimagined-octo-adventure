import os
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional, List
import motor.motor_asyncio

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.catworld


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
    strength: float = Field(..., le=100.0)

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


class UpdateCatModel(BaseModel):
    catname: Optional[str]
    skill: Optional[str]
    strength: Optional[float]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "catname": "Kitty Lilly",
                "skill": "Drinks Seawater, Knows How To Deal With Hairballs",
                "strength": "13.0",
            }
        }


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
