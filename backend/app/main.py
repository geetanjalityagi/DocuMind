from fastapi import FastAPI

from app.api.routes.documents import router as document_router
from app.api.routes.chat import router as chat_router

app = FastAPI()

app.include_router(document_router)

app.include_router(chat_router)

@app.get('/')
def run():
    return "Hello"
