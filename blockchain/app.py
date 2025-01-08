from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.end_points import router
from utils.utxo_operations import UTXO_Operation
from utils.block_functions import Blockchain
from models import Transaction
from typing import List

"""
ProgramFlow:
    Prior to any process, the block_chain is initialized with a genesis block
    1. Transactions are created and stored in request.app.open_transactions through the 'new-transaction' endpoint
    2. When Someone wants to mine a block they will verify the transactions and do the proof of work(mining) and the endpoint 
       that does mining , i.e. mine-block, returns the mined block
    3. The miner then passes this mined block to the add-block endpoint and this ends the process by appending the mined block to the block_chain

    !!!!! ##The End points are in the end_points file within the routes directory
"""
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