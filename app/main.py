from fastapi import FastAPI,status
from .schemas.message import CreateMessageRequest
from app.db.database import check_database_connection

app = FastAPI(
    title="ContextForge"
)


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }



@app.post(
    "/messages",
    status_code=status.HTTP_201_CREATED
)
def create_message(request: CreateMessageRequest):
    message = message_service.create_message(request)
    return message.to_dict()


@app.get("/db-health")
def database_health_check():
    check_database_connection()
    return {"database": "connected"}