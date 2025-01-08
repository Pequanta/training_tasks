from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.end_points import router
from helper_functions.utxo_operations import UTXO_Operation
from helper_functions.block_functions import Blockchain
from models import Transaction
from typing import List


CORSMiddleware
origins = [
    "*"
    ]
def lifespan(app: FastAPI):
    #The following initializations create a block chain list and a utxo set that will be used throughout the application
    app.block_chain = Blockchain()
    app.utxo_set = UTXO_Operation()
    #Until the mining is done , the transactions pend in the following list
    app.open_transactions = List[Transaction]
    yield
    app.block_chain.chain.clear()

app = FastAPI(lifespan=lifespan)
app.include_router(router, prefix="/block-chain", tags=["block-chain"])
app.add_middleware(
    CORSMiddleware, 
    allow_origins = origins, 
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)