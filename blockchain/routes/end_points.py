from fastapi import APIRouter, Request, HTTPException
from helper_functions.block_functions import Blockchain
from models import Blockchain, Transaction, Hash
from pydantic import Field
router = APIRouter()


@router.get("/chain")
async def get_current_chain(request: Request) -> Blockchain:
    try:
        return request.app.blockchain
    except:
        return HTTPException(status_code=404)

@router.post("/mine-block")
async def mine_block(request: Request, index: int, previous_hash: Hash, timestamp: str, data: Tr):
    nonce = 0 
    hash_result = request.app.block_chain.hash_block(index, previous_hash, timestamp, data, nonce)
    while not hash_result.startswith('000'):
        nonce += 1
        hash_result = request.app.block_chain.hash_block(index, previous_hash, timestamp, data, nonce)
    return nonce, hash_result
@router.post("/new-transaction")
async def add_new_transaction(request: Request, sender: str, receiver: str, input_utxos: UTXO, output_utxos: UTXO, signature) -> bool:
    try:
        if block in request.app.block_chain:
            block.add()
    except:
        raise HTTPException(status_code=401, description="Could not able to add the transaction")
@router.post("/add-block")
async def add_new_block(request: Request, block: Field(...)) -> bool:
    try:
        block_ = Block(**block)
        if block_ not in request.app.block_chain:
            return block_
        else:
            return {"message": "The block already exists in the pool"}
    except:
        raise HTTPException(status_code=404)