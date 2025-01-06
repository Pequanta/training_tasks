from fastapi import APIRouter, Request, HTTPException
from helper_functions.block_functions import Blockchain
from models import Blockchain, Transaction
router = APIRouter()


@router.get("/chain")
async def get_current_chain(request: Request) -> Blockchain:
    try:
        current_chain = request.app.block_chain.peak()
        return current_chain
    except:
        return HTTPException(status_code=404)

@router.post("/mine_block")
async def mine_block(request: Request, index, previous_hash, timestamp, data):
    nonce = 0 
    hash_result = block_chain.hash_block(index, previous_hash, timestamp, data, nonce)
    while not hash_result.startswith('000'):
        nonce += 1
        hash_result = block_chain.hash_block(index, previous_hash, timestamp, data, nonce)
    return nonce, hash_result
@router.post("/new-transaction")
async def add_new_transaction(request: Request, transaction: Transaction) -> bool:
    try:
        return True
    except:
        raise HTTPException(status_code=401, description="Could not able to add the transaction")
@router.post("/add_block")
async def add_new_block(request: Request) -> bool:
    try:
        return 
    except: