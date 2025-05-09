from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.sshPayloadsRoutes import router as ssh_payloads_router

app = FastAPI(
    title="... API",
    description="API pour le logiciel ...",
    version="0.0.1",
    docs_url=None,
    redoc_url=None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ssh_payloads_router)

@app.get("/")
async def read_root():
    return {
        "message": "Bienvenue sur l'API ...!",
        "version": "0.0.1",
        "status": "online"
    }
