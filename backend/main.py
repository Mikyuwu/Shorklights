from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from routes.sshPayloadsRoutes import router as ssh_payloads_router
from routes.serversRoutes import router as servers_router

from helpers.returnResult import return_result
from database.dbHelper import init_db


init_db()

app = FastAPI(
    title="... API",
    description="API pour le logiciel Shorklights",
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
app.include_router(servers_router)

@app.get("/")
async def read_root():
    return {
        "message": "Bienvenue sur l'API Shorklights!",
        "version": "0.0.1",
        "status": "online"
    }

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return return_result(False, message=f"{exc.errors()[0]['msg']}", status_code=400)