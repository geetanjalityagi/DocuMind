from fastapi import FastAPI

from app.api.routes.documents import router as document_router
app = FastAPI()

app.include_router(document_router)

@app.get('/')
def run():
    return "Hello"