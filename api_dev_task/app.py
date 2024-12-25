from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
from motor.motor_asyncio import AsyncIOMotorClient
from routes.users import router as users
from routes.products import router as products



DB_URL=config('DB_URL', str)
DB_NAME=config('DB_NAME', str)

CORSMiddleware
origins = [
    "*"
    ]
def lifespan(app: FastAPI):
    app.mongodb_client = AsyncIOMotorClient(DB_URL)
    app.mongodb = app.mongodb_client[DB_NAME]
    yield
    app.mongodb.client.close()

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
