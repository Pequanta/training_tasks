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
    """
    Represents a single transaction in the blockchain.
    """
    transaction_id: str = Field(..., description="Unique identifier for the transaction.")
    sender: str = Field(..., description="Public key or address of the sender initiating the transaction.")
    reciever: str = Field(..., description="Public key or address of the receiver.")
    inputs: List["UTXO"] = Field(..., description="List of UTXOs used as inputs for the transaction.")
    outputs: List["UTXO"] = Field(..., description="List of UTXOs created as outputs from the transaction.")
    timestamp: datetime = Field(..., description="Timestamp indicating when the transaction was created.")
    amount: float = Field(..., ge=0, description="Amount of cryptocurrency being transferred.")
    signature: str = Field(..., description="Digital signature of the transaction, ensuring its authenticity.")

class Block(BaseModel):
    """
    Represents a block in the blockchain.
    """
    index: int = Field(..., description="Index of the block in the blockchain.")
    timestamp: datetime = Field(..., description="Timestamp when the block was created.")
    transactions: List[Transaction] = Field(..., description="List of transactions included in the block.")
    previous_hash: str = Field(..., description="Hash of the previous block in the chain.")
    nonce: int = Field(..., description="Nonce used in the proof-of-work algorithm for mining the block.")
    hash: str = Field(..., description="Hash of the current block.")

class Wallet(BaseModel):
    """
    Represents a user's wallet for managing cryptocurrency.
    """
    address: str = Field(..., description="Unique address of the wallet, derived from the public key.")
    private_key: str = Field(..., description="Private key for signing transactions.")
    public_key: str = Field(..., description="Public key for verifying transactions and generating the wallet address.")

class Blockchain(BaseModel):
    """
    Represents the blockchain and its core properties.
    """
    chain: List[Block] = Field(..., description="List of all blocks in the blockchain.")
    difficulty: int = Field(..., ge=0, description="Difficulty level for mining new blocks.")
    pending_transactions: List[Transaction] = Field(default_factory=list, description="List of transactions awaiting inclusion in a mined block.")