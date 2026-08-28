from uuid import uuid4

from sqlalchemy.orm import Session

from app.db.models import UserModel


class UserRepository:
    def save(
        self,
        db: Session,
        email: str,
        display_name: str,
    ) -> UserModel:
        row = UserModel(
            id=str(uuid4()),
            email=email,
            display_name=display_name,
        )

        db.add(row)
        db.commit()
        db.refresh(row)

        return row
    
    def find_by_id(
        self,
        db: Session,
        user_id: str,
    ) -> UserModel | None:
        return db.get(UserModel, user_id)