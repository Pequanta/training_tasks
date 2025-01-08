from typing import List, Set,Optional
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class UTXO(BaseModel):
    """Represents an unspent transaction output (UTXO)."""
    transaction_id: UUID = Field(..., description="Transaction ID where the UTXO was created.")
    index: int = Field(..., description="Index of the output in the transaction.")
    value: int = Field(..., ge=0, description="Amount of cryptocurrency in satoshis (or smallest unit).")
    address: str = Field(..., description="Public key or address associated with this UTXO.")
    confirmed: bool = Field(default=True, description="Whether the UTXO is confirmed in the blockchain.")
    spent: bool = Field(default=False, description="Whether the UTXO has been spent.")

class UTXOSet(BaseModel):
    """Represents a collection of UTXOs."""
    utxos: Set[UTXO] = Field(default_factory=list, description="List of UTXOs.")

class Transaction(BaseModel):
    transaction_id: str
    sender: str
    reciever: str
    inputs: List[UTXO]
    outputs: List[UTXO]
    timestamp: datetime
    amount: float
    signature: str

class Block(BaseModel):
    index: int
    timestamp: datetime
    transactions: List[Transaction]
    previous_hash: str
    nonce: int
    hash: str
class Wallet(BaseModel):
    address: str
    private_key: str
    public_key: str

class Blockchain(BaseModel):
    chain: List[Block]
    difficulty: int
    pending_transactions: List[Transaction]