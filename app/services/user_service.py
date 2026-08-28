from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.schemas.user import CreateUserRequest


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def create_user(
        self,
        db: Session,
        request: CreateUserRequest,
    ) -> dict:
        row = self.repository.save(
            db,
            request.email,
            request.display_name,
        )

        return {
            "id": row.id,
            "email": row.email,
            "display_name": row.display_name,
            "created_at": row.created_at.isoformat(),
        }
        
    def get_user(
        self,
        db: Session,
        user_id: str,
    ) -> dict:
        row = self.repository.find_by_id(db, user_id)

        if row is None:
            raise LookupError("user not found")

        return {
            "id": row.id,
            "email": row.email,
            "display_name": row.display_name,
            "created_at": row.created_at.isoformat(),
        }