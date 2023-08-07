import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return hashlib.sha256(
            str(self.index).encode() +
            str(self.previous_hash).encode() +
            str(self.timestamp).encode() +
            str(self.data).encode() +
            str(self.nonce).encode()
        ).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

        print("Block mined:", self.hash)

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4

    def create_genesis_block(self):
        return Block(0, "0", int(time.time()), "Genesis Block")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
            if not self.is_proof_valid(current_block, self.difficulty):
                return False

        return True

    def is_proof_valid(self, block, difficulty):
        return block.hash[:difficulty] == "0" * difficulty

if __name__ == '__main__':
    blockchain = Blockchain()

    print("Mining block 1...")
    blockchain.add_block(Block(1, "", int(time.time()), {"amount": 10}))

    print("Mining block 2...")
    blockchain.add_block(Block(2, "", int(time.time()), {"amount": 5}))

    print("Is blockchain valid?", blockchain.is_chain_valid())
