from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    email: str
    display_name: str