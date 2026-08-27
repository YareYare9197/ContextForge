from app.domain.message import Message


class MessageService:
    def __init__(self):
        self.messages = {}

    def create_message(self, request):
        message = Message(
            conversation_id=request.conversation_id,
            role=request.role,
            content=request.content,
            sender_id=request.sender_id,
            model_name=request.model_name
        )

        self.messages[message.id] = message
        return message