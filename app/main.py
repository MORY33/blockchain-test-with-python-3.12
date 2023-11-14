from fastapi import FastAPI, WebSocket, Depends
from fastapi.middleware.cors import CORSMiddleware
from api.v1.routers.blockchain_urls import bc_router
from models.blockchain_models import Blockchain

app = FastAPI(title='Blockchain API', version='1.0.0')
blockchain = Blockchain()

#initialize middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(bc_router, prefix="/blockchain", tags=["Blockchain Operations"])


