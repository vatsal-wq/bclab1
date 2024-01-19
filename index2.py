import hashlib
import datetime as date

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def to_dict(self):
        return {
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount
        }

class Block:
    def __init__(self, previous_hash, transactions):
        self.timestamp = date.datetime.now()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.merkle_root = self.calculate_merkle_root()
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_merkle_root(self):
        transaction_hashes = [hashlib.sha256(str(tx.to_dict()).encode()).hexdigest() for tx in self.transactions]

        while len(transaction_hashes) > 1:
            new_hashes = []
            for i in range(0, len(transaction_hashes)-1, 2):
                combined_hash = hashlib.sha256((transaction_hashes[i] + transaction_hashes[i+1]).encode()).hexdigest()
                new_hashes.append(combined_hash)

            if len(transaction_hashes) % 2 == 1:
                new_hashes.append(transaction_hashes[-1])

            transaction_hashes = new_hashes

        return transaction_hashes[0]

    def calculate_hash(self):
        block_string = str(self.timestamp) + str(self.merkle_root) + str(self.previous_hash) + str(self.nonce)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

    def to_dict(self):
        return {
            'timestamp': self.timestamp,
            'merkle_root': self.merkle_root,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce,
            'hash': self.hash,
            'transactions': [tx.to_dict() for tx in self.transactions]
        }

# Example Usage
if __name__ == "__main__":
    # Create some transactions
    transaction1 = Transaction("Alice", "Bob", 10)
    transaction2 = Transaction("Bob", "Charlie", 5)
    transaction3 = Transaction("Vatsal", "Om", 10)
    transaction4 = Transaction("Om", "Vatsal", 5)
    transactions = [transaction1, transaction2, transaction3, transaction4]

    # Create a genesis block with a random previous hash
    genesis_block = Block("0", transactions)
    genesis_block.mine_block(2)

    # Create a new block with the hash of the genesis block as the previous hash
    new_transactions = [Transaction("Charlie", "David", 3), Transaction("David", "Alice", 7)]
    new_block = Block(genesis_block.hash, new_transactions)
    new_block.mine_block(2)

    # Display blocks
    print("Genesis Block:")
    print(genesis_block.to_dict())

    print("\nNew Block:")
    print(new_block.to_dict())
