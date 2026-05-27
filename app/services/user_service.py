"""
User service layer.

Contains business logic for user management.
"""

import logging
import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import User
from app.repositories import UserRepository
from app.schemas import UserCreate, UserUpdate

logger = logging.getLogger(__name__)


def get_all_users(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> tuple[int, list[User]]:
    """
    Retrieve paginated users.

    Args:
        db: Active database session
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        Tuple containing:
        - Total user count
        - Paginated user list
    """

    # Retrieve total number of users
    total = UserRepository.count(db)

    # Retrieve paginated users
    users = UserRepository.get_all(
        db=db,
        skip=skip,
        limit=limit,
    )

    logger.info(
        "Retrieved %d users (skip=%d, limit=%d)",
        len(users),
        skip,
        limit,
    )

    return total, users


def get_user_by_id(
    db: Session,
    user_id: str,
) -> User:
    """
    Retrieve a user by ID.

    Args:
        db: Active database session
        user_id: User UUID

    Returns:
        User instance

    Raises:
        HTTPException: If the user does not exist
    """

    # Retrieve user from repository
    user = UserRepository.get_by_id(db, user_id)

    # Validate user existence
    if not user:

        logger.warning(
            "User not found: id=%s",
            user_id,
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id '{user_id}' was not found.",
        )

    return user


def create_user(
    db: Session,
    data: UserCreate,
) -> User:
    """
    Create a new user.

    Args:
        db: Active database session
        data: User creation payload

    Returns:
        Created user instance

    Raises:
        HTTPException: If username or email already exists
    """

    # Validate username uniqueness
    existing_username = UserRepository.get_by_username(
        db,
        data.username,
    )

    if existing_username:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Username '{data.username}' is already in use.",
        )

    # Validate email uniqueness
    existing_email = UserRepository.get_by_email(
        db,
        data.email,
    )

    if existing_email:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email '{data.email}' is already registered.",
        )

    # Current UTC timestamp
    now = datetime.now(timezone.utc)

    # Create ORM entity
    user = User(
        id=str(uuid.uuid4()),
        created_at=now,
        updated_at=now,
        **data.model_dump(),
    )

    # Persist user
    created_user = UserRepository.create(
        db=db,
        user=user,
    )

    logger.info(
        "User created successfully: id=%s username=%s",
        created_user.id,
        created_user.username,
    )

    return created_user


def update_user(
    db: Session,
    user_id: str,
    data: UserUpdate,
) -> User:
    """
    Partially update an existing user.

    Args:
        db: Active database session
        user_id: User UUID
        data: Fields to update

    Returns:
        Updated user instance

    Raises:
        HTTPException:
            - 404 if the user does not exist
            - 409 if username or email already exists
    """

    # Validate user existence
    user = get_user_by_id(db, user_id)

    # Extract only explicitly provided fields
    updates = data.model_dump(exclude_unset=True)

    # Validate username uniqueness
    if (
        "username" in updates
        and updates["username"] != user.username
    ):

        existing_username = UserRepository.get_by_username(
            db,
            updates["username"],
        )

        if existing_username:

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Username '{updates['username']}' is already in use.",
            )

    # Validate email uniqueness
    if (
        "email" in updates
        and updates["email"] != user.email
    ):

        existing_email = UserRepository.get_by_email(
            db,
            updates["email"],
        )

        if existing_email:

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Email '{updates['email']}' is already registered.",
            )

    # Apply dynamic field updates
    for field, value in updates.items():
        setattr(user, field, value)

    # Update modification timestamp
    user.updated_at = datetime.now(timezone.utc)

    # Persist updates
    updated_user = UserRepository.update(
        db=db,
        user=user,
    )

    logger.info(
        "User updated successfully: id=%s updated_fields=%s",
        user_id,
        list(updates.keys()),
    )

    return updated_user


def delete_user(
    db: Session,
    user_id: str,
) -> dict:
    """
    Delete a user.

    Args:
        db: Active database session
        user_id: User UUID

    Returns:
        Success confirmation message

    Raises:
        HTTPException: If the user does not exist
    """

    # Validate user existence
    user = get_user_by_id(db, user_id)

    # Delete user from repository
    UserRepository.delete(
        db=db,
        user=user,
    )

    logger.info(
        "User deleted successfully: id=%s",
        user_id,
    )

    return {
        "detail": f"User '{user_id}' deleted successfully.",
    }