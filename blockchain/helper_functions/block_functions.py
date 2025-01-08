import hashlib
import time
from models import Block, Transaction
from typing import List
class Blockchain:
    def __init__(self, difficulty=3):
        self.chain = []
        self.difficulty = difficulty
        self.create_genesis_block()

    def create_genesis_block(self):
        # Creating the first block (genesis block)
        cont_data = {"index": 0, "timestamp" : int(time.time()), "transactions": [], "previous_hash": "", "nonce": 0, "hash": ""}
        genesis_block = Block(**cont_data)
        self.chain.append(genesis_block)

    def hash_data(self,data, nonce, previous_hash):
        """
        This method takes the block's information and generates a hash.
        The hashing algorithm used here is SHA-256.
        """
        cont_data = ""
        for data_val in data:
            cont_data += str(data_val)
        block_string = f"{cont_data}{nonce}{previous_hash}".encode('utf-8')
        return hashlib.sha256(block_string).hexdigest()

    def mine(self, data, previous_hash):
        """
        This method finds the correct nonce for the block such that the hash has leading zeros equal to the difficulty.
        """
        nonce = 0
        hash_result = self.hash_data(data, nonce, previous_hash)
        # Mine until we find a hash with the required number of leading zeros
        while not hash_result.startswith('0' * self.difficulty):
            nonce += 1
            hash_result = self.hash_data(data, nonce, previous_hash)

        return nonce, hash_result

    def add_block(self, data):
        last_block = self.chain[-1]
        new_index = last_block.index + 1
        new_timestamp = int(time.time())

        data["timestamp"] = str(new_timestamp)
        data["previous_hash"] = data["previous_hash"] 
        data["index"] = new_index
        # Mine a new block with the given data
        nonce, new_hash = self.mine(data, data["previous_hash"])
        data["nonce"] = nonce 
        data["hash"] = new_hash

        # Creating new block and adding it to the chain
        new_block = Block(**data)
        return new_block

