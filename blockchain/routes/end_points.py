from fastapi import APIRouter, Request, HTTPException
from fastapi.encoders import jsonable_encoder
from models import Block, Wallet, Transaction
from typing import List
from utils import key_functions

router = APIRouter()



"""
Description for the methods: 

-> get_current_chain(request: Request) 
    Fetches the current blockchain. This endpoint retrieves the list of blocks that 
    make up the blockchain stored in the application's state.

-> mine_block(request: Request, block: Block)
    Handles the mining of a new block. This endpoint takes a block object, validates its 
    transactions, and attempts to mine it by finding a valid hash. The mined block's hash 
    is appended to the block data and returned. 

-> add_new_transaction(request: Request, amount: float, sender: str, reciever: str, user_data: Wallet, transaction_id: str )
    Creates and validates a new transaction between two parties. It checks the sender's balance, 
    gathers the required UTXOs, and constructs a new transaction with inputs, outputs, and a digital signature.
-> add_new_block(request: Request, block: Block)
    Adds a newly created block to the blockchain if it is valid. It checks whether the block's
    hash satisfies the required difficulty level (starts with "000") before appending it to the chain.
"""
@router.get("/chain")
async def get_current_chain(request: Request) -> List:
    try:
        return request.app.block_chain.chain
    except:
        return HTTPException(status_code=404)

@router.post("/mine-block")
async def mine_block(request: Request, block: Block):
    try:
        block = jsonable_encoder(block)
        for transaction in request.app.open_transactions:
            data = {key: value for key, value in transaction.items() if key != "siganture"}
            for utxo in transaction["outputs"]:
                if not key_functions.verify_message(data, transaction["signature"],  utxo.address):
                    break
            block["transactions"].append(transaction)
        hash = request.app.block_chain.mine(request, block)
        block["hash"] = hash[1]
        return block
    except:
        raise HTTPException(status_code=404)
   
@router.post("/new-transaction")
async def add_new_transaction(request: Request, amount: float,reciever: str,  sender: str, reciever_public_key: str, user_data: Wallet, transaction_id: str) -> Transaction:
    try:
        #The transactions are done based on the defined model in the models.py
        user_utxos = request.app.utxo_set.get_utxos_by_address(user_data["public_key"])
        user_balance = request.app.utxo_set.get_balance(user_data["public_key"])
        output_utxos = []
        reciever_utxo = set()
        if user_balance > amount:
            sum_cont = 0
            for utxo in user_utxos:
               if sum_cont >= amount:
                    return {"message": "successful transaction"}
               sum_cont += utxo["amount"]
               ##If the utxos are spent , they will be assinged spent to make sure they are not used for another transaction 
               utxo.spent = True
               output_utxos.append(utxo)
               ##After the output utxos are spent the reciever will claim the utxos
               utxo.address = reciever_utxo
               reciever_utxo.add(utxo)
        else:
            return {"Message" : "insufficient amount for transaction"}
        transaction = {"id": transaction_id, "sender": sender, "reciever": reciever}
        transaction["inputs"] = user_utxos
        transaction["outputs"] = output_utxos
        transaction["signature"] = key_functions.sign_in_with_key(transaction["private_key"], transaction)
        for utxo in reciever_utxo:
            request.app.utxo_set.add(utxo)

        return request.app.open_transactions(Transaction(**transaction))
    except:
        raise HTTPException(status_code=401, detail="Could not able to add the transaction")
@router.post("/add-block")
async def add_new_block(request: Request, block: Block):
    #The block should be added after its mined, if it isn't the method returns an error
    try:
        if block.hash.startswith("000"):
            request.app.block_chain.chain.append(block)
        else:
            return {"message": "The block is not valid and needs to be mined"}
        return {"hash_value": block["hash"]}
    except:
        raise HTTPException(status_code=404)