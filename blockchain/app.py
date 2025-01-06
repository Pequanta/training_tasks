from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.end_points import router


CORSMiddleware
origins = [
    "*"
    ]
def lifespan(app: FastAPI):
    app.block_chain = {}
    yield
    app.block_chain.clear()

app = FastAPI(lifespan=lifespan)
app.include_router(router, prefix="/block-chain", tags=["block-chain"])
app.add_middleware(
    CORSMiddleware, 
    allow_origins = origins, 
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)