from typing import List, Optional
from dataclasses import dataclass, field
from fastapi import FastAPI, HTTPException, Body
from time import time
import hashlib
import json


@dataclass
class Transaction:
    sender: str
    recipient: str
    amount: int

    def to_dict(self):
        # Convert transaction to a dict
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount
        }

@dataclass
class Block:
    index: int
    timestamp: float
    transactions: List[Transaction]
    proof: int
    previous_hash: str

    def to_dict(self):
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [t.to_dict() for t in self.transactions],
            'proof': self.proof,
            'previous_hash': self.previous_hash
        }

@dataclass
class Blockchain:
    chain: List[Block] = field(default_factory=list)
    current_transactions: List[Transaction] = field(default_factory=list)

    def __post_init__(self):
        #Create genesis block
        self.new_block(proof=100, previous_hash="1")

    def new_block(self, proof: int, previous_hash: Optional[str] = None) -> Block:
        block = Block(
            index=len(self.chain) + 1,
            timestamp=time(),
            transactions=self.current_transactions,
            proof=proof,
            previous_hash=previous_hash or self.hash(self.chain[-1]),
        )
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender: str, recipient: str, amount: int) -> int:
        transaction = Transaction(sender, recipient, amount)
        self.current_transactions.append(transaction)
        return self.last_block.index + 1

    @staticmethod
    def hash(block):
        block_string = json.dumps(block.to_dict(), sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    def proof_of_work(self, last_proof: int) -> int:
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof: int, proof: int) -> bool:
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
