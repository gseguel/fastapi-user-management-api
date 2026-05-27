"""User persistence layer."""

from sqlalchemy.orm import Session

from app.models import User


class UserRepository:
    """User database operations."""

    @staticmethod
    def count(db: Session) -> int:
        """Return total users."""

        return db.query(User).count()

    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[User]:
        """Return paginated users."""

        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(
        db: Session,
        user_id: str,
    ) -> User | None:
        """Return user by ID."""

        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_by_username(
        db: Session,
        username: str,
    ) -> User | None:
        """Return user by username."""

        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_by_email(
        db: Session,
        email: str,
    ) -> User | None:
        """Return user by email."""

        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create(
        db: Session,
        user: User,
    ) -> User:
        """Create a user."""

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def update(
        db: Session,
        user: User,
    ) -> User:
        """Update a user."""

        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def delete(
        db: Session,
        user: User,
    ) -> None:
        """Delete a user."""

        db.delete(user)
        db.commit()