import os
import datetime
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from pydantic import Field
from enum import IntEnum
from bson import ObjectId
from typing import Optional, List
import motor.motor_asyncio


app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.test_api


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


class Status(IntEnum):
    current = 1
    stable = 2
    deprecated = 2


class Format(IntEnum):
    JSON = 1
    protobuf = 2


class VersionModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now)
    name: str = Field(..., alias="s_name")
    version_number: str = Field(...)
    status: Status = Field(default=Status.current)
    user_id: PyObjectId = Field(...)


class UserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    owner: bool = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class SStorageModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    sversion_id: PyObjectId = Field(...)
    format: Format = Field(...)
    original_filesize: float = Field(...)
    md5: str = Field(...)
    s: str = Field(...)


class SFieldsModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    sversion_id: PyObjectId = Field(...)
    field_name: str = Field(...)
    format: Format = Field(...)
    required: bool = Field(...)
    nested: bool = Field(...)
    f: Optional[dict] = Field(...)


@app.post(
    "/UserInsert", response_description="Add User and Owner", response_model=UserModel
)
async def create_user(user: UserModel = Body(...)):
    user = jsonable_encoder(user)
    new_user = await db["users"].insert_one(user)
    created_user = await db["users"].find_one({"_id": new_user.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_cat)


@app.get("/Users", response_description="List all Users and Owners")
async def list_users():
    users = await db["users"].find().to_list(1000)
    return users


@app.get("/SVersion", response_description="List all Versions of all Ss")
async def list_versions():
    s_versions = await db["s_versions"].find().to_list(1000)
    return s_versions


@app.get("/SF", response_description="List Schema field relations")
async def list_fields():
    s_fields = await db["s_fields"].find().to_list(1000)
    return s_fields


@app.get("/SStorage", response_description="Storage list")
async def list_storage():
    s_storage = await db["s_storage"].find().to_list(1000)
    return s_storage
