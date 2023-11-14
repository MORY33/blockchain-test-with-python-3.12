from fastapi import HTTPException, APIRouter, Depends
from models.blockchain_models import Blockchain, Body, Transaction

bc_router = APIRouter()


def get_blockchain():
    from main import blockchain
    return blockchain

@bc_router.post("/transactions/new")
async def new_transaction(
    transaction: Transaction = Body(..., example={"sender": "alice", "recipient": "bob", "amount": 5}),
    blockchain: Blockchain = Depends(get_blockchain)
):
    index = blockchain.new_transaction(transaction.sender, transaction.recipient, transaction.amount)
    return {"message": f"Transaction will be added to Block {index}"}

@bc_router.get("/mine")
async def mine(blockchain: Blockchain = Depends(get_blockchain)):
    last_block = blockchain.last_block
    last_proof = last_block.proof
    proof = blockchain.proof_of_work(last_proof)

    blockchain.new_transaction(
        sender="0",
        recipient="node_identifier",
        amount=1,
    )

    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block.index,
        'transactions': [t.__dict__ for t in block.transactions],
        'proof': block.proof,
        'previous_hash': block.previous_hash,
    }
    return response


@bc_router.get("/chain")
async def full_chain(blockchain: Blockchain = Depends(get_blockchain)):
    response = {
        'chain': [block.__dict__ for block in blockchain.chain],
        'length': len(blockchain.chain),
    }
    return response