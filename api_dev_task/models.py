from pydantic import BaseModel
from typing import List
from bson import ObjectId
from pydantic import BaseModel, Field
class PyObjectId(ObjectId):
        @classmethod
        def __get_validators__(cls):
                yield cls.validate
        @classmethod
        def validate(cls, v, field=None):
                if not ObjectId.is_valid(v):
                        raise ValueError("Invalid objectid")
                return ObjectId(v)
        @classmethod
        def __modify_schema(cls, field_schema):
                field_schema.update(type="string")
class MongoBaseModel(BaseModel):
        id: PyObjectId = Field(default_factory=PyObjectId , alias="_id")
        class Config:
                json_encoders = {ObjectId: str}

class UserBase(MongoBaseModel):
        user_name: str
class ProductBase(MongoBaseModel):
        product_name: str
        product_price: float
class ProductDataModel(ProductBase):
        pass
class UserDataModel(UserBase):
        purchased_products: List[str]