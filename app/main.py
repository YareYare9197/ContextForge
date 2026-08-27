from fastapi import FastAPI

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