from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID
from pydantic import BaseModel
from typing import List, Set
from datetime import datetime
import hashlib


def hash_data(data: str) -> str:
    """Hash data using SHA256."""
    return hashlib.sha256(data.encode()).hexdigest()


class Proof(BaseModel):
    """Represents a proof for a UTXO in the accumulator."""
    value: str
    proof_path: List[str] = Field(default_factory=list)

    def verify(self, root: str) -> bool:
        """Verify the proof against the accumulator's root."""
        current_hash = self.value
        for sibling in self.proof_path:
            combined = sorted([current_hash, sibling])  # Ensure consistent order
            current_hash = hash_data(combined[0] + combined[1])
        return current_hash == root

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

class TransactionInput(BaseModel):
    transaction_id: str
    output_index: int
    signature: str

class TransactionOutput(BaseModel):
    recipient: str
    amount: float
    output_index: int

class Transaction(BaseModel):
    transaction_id: str
    inputs: List[TransactionInput]
    outputs: List[TransactionOutput]
    timestamp: datetime

class Block(BaseModel):
    index: int
    timestamp: datetime
    transactions: List[Transaction]
    previous_hash: str
    nonce: int
    hash: str

class UTXO(BaseModel):
    transaction_id: str
    output_index: int
    recipient: str
    amount: float
    spent: bool = False

class Wallet(BaseModel):
    address: str
    private_key: str
    public_key: str

class Blockchain(BaseModel):
    chain: List[Block]
    difficulty: int
    pending_transactions: List[Transaction]

class Node(BaseModel):
    node_id: str
    host: str
    port: int
    peers: List["Node"]
