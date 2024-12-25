from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING
from routes.users import router as users
from routes.products import router as products
from redis.asyncio import Redis
DB_URL = config('DB_URL', str)
DB_NAME= config('DB_NAME', str)





CORSMiddleware
origins = [
    "*"
    ]
async def lifespan(app: FastAPI):
    app.mongodb_client = AsyncIOMotorClient(DB_URL)
    app.mongodb = app.mongodb_client[DB_NAME]
    await app.mongodb["products"].create_index([("product_name", ASCENDING)], unique=True)
    await app.mongodb["users"].create_index([("user_name", ASCENDING)], unique=True)
    app.redis  = await Redis(host="localhost",port=6379,  decode_responses=True)
    yield
    app.mongodb.client.close()
    await app.redis.close()

app = FastAPI(lifespan=lifespan)
app.include_router(users, prefix="/users", tags=["users"])
app.include_router(products, prefix="/products", tags=["products"])
app.add_middleware(
    CORSMiddleware, 
    allow_origins = origins, 
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)
