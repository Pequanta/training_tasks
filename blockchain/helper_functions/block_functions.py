import hashlib
import time
from models import Block
class Blockchain:
    def __init__(self, difficulty=3):
        self.chain = []
        self.difficulty = difficulty
        self.create_genesis_block()

    def create_genesis_block(self):
        # Creating the first block (genesis block)
        genesis_block = Block(0, "0", int(time.time()), "Genesis Block", self.hash_block(0, "0", int(time.time()), "Genesis Block", 0), 0)
        self.chain.append(genesis_block)

    def hash_block(self, index, previous_hash, timestamp, data, nonce):
        """
        This method takes the block's information and generates a hash.
        The hashing algorithm used here is SHA-256.
        """
        block_string = f"{index}{previous_hash}{timestamp}{data}{nonce}".encode('utf-8')
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, index, previous_hash, timestamp, data):
        """
        This method finds the correct nonce for the block such that the hash has leading zeros equal to the difficulty.
        """
        nonce = 0
        hash_result = self.hash_block(index, previous_hash, timestamp, data, nonce)

        # Mine until we find a hash with the required number of leading zeros
        while not hash_result.startswith('0' * self.difficulty):
            nonce += 1
            hash_result = self.hash_block(index, previous_hash, timestamp, data, nonce)

        return nonce, hash_result

    def add_block(self, data):
        last_block = self.chain[-1]
        new_index = last_block.index + 1
        new_timestamp = int(time.time())

        # Mine a new block with the given data
        nonce, new_hash = self.mine_block(new_index, last_block.hash, new_timestamp, data)

        # Creating new block and adding it to the chain
        new_block = Block(new_index, last_block.hash, new_timestamp, data, new_hash, nonce)
        self.chain.append(new_block)

    def print_blockchain(self):
        for block in self.chain:
            print(f"Block {block.index}:")
            print(f"  Previous Hash: {block.previous_hash}")
            print(f"  Timestamp: {block.timestamp}")
            print(f"  Data: {block.data}")
            print(f"  Hash: {block.hash}")
            print(f"  Nonce: {block.nonce}\n")


# # Example usage:
# blockchain = Blockchain(difficulty=3)
# blockchain.add_block("First transaction data")
# blockchain.add_block("Second transaction data")

# blockchain.print_blockchain()
