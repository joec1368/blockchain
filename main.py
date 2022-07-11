import time
import hashlib


class Transaction:
    def __init__(self, sender, receiver, amounts, fee, message):
        self.sender = sender;
        self.receiver = receiver
        self.amounts = amounts
        self.fee = fee
        self.message = message


class Block:
    def __init__(self, previous_hash, difficulty, miner, miner_rewards):
        self.previous_hash = previous_hash
        self.hash = ''
        self.difficulty = difficulty
        self.nonce = 0
        self.timestamp = int(time.time())
        self.transactions = []
        self.miner = miner
        self.miner_rewards = miner_rewards


class BlockChain:
    def __init__(self):
        self.adjust_difficulty_blocks = 10
        self.difficulty = 1
        self.block_time = 30
        self.mining_rewards = 10
        self.blcok_limitation = 32
        self.chain = []
        self.pending_transactions = []

    def transaction_to_string(self, transaction):  # 把transaction 轉換成字串
        transaction_dict = {
            'sender': str(transaction.sender),
            'receiver': str(transaction.receiver),
            'amounts': transaction.amounts,
            'message': transaction.message
        }
        return str(transaction_dict)

    def get_transactions_string(self, block):  # 把區塊紀錄內的所有交易明細轉換成一個字串
        transaction_str = ''
        for transaction in block.transactions:
            transaction_str += self.transaction_to_string(transaction)
        return transaction_str

    def get_hash(self, block, nonce):
        s = hashlib.sha1()
        s.update(
            (
                    block.previous_hash
                    + str(block.timestamp)
                    + self.get_transactions_string(block)
                    + str(nonce)
            ).encode("utf-8")
        )
        h = s.hexdigest()
        return h

    def create_genesis_block(self):
        print("create genesis block...")
        new_block = Block("First", self.difficulty, 'abc', self.mining_rewards)
        new_block.hash = self.get_hash(new_block, 0)
        self.chain.append(new_block)

    def add_transaction_to_block(self, block):
        # Get the transaction with the highest fee by block_limitation
        self.pending_transactions.sort(key=lambda x: x.fee, reverse=True)
        if len(self.pending_transactions) > self.blcok_limitation:
            transactions_accepted = self.pending_transactions[:self.blcok_limitation]
            self.pending_transactions = self.pending_transactions[self.blcok_limitation:]
        else:
            transactions_accepted = self.pending_transactions
            self.pending_transactions = []
        block.transactions = transactions_accepted

    def mine_block(self, miner):
        start = time.process_time()
        last_block = self.chain[-1]
        new_block = Block(last_block.hash, self.difficulty, miner, self.mining_rewards)

        self.add_transaction_to_block(new_block)
        new_block.previous_hash = last_block.hash
        new_block.difficulty = self.difficulty
        new_block.hash = self.get_hash(new_block,new_block.nonce)

        while new_block.hash[0:self.difficulty] != '0' * self.difficulty:
            new_block.nonce += 1
            new_block.hash = self.get_hash(new_block,new_block.nonce)

        time_consumed = round(time.process_time() - start,5)
        print(f"Hash found : {new_block.hash} @ difficulty {self.difficulty},time cost {time_consumed}s")
        self.chain.append(new_block)
