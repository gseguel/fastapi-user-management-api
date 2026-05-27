"""User management endpoints."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas import (
    UserCreate,
    UserListResponse,
    UserResponse,
    UserUpdate,
)
from app.services import user_service

router = APIRouter(prefix="/users")


@router.get(
    "/",
    response_model=UserListResponse,
    summary="List users",
    description=(
        "Retrieve a paginated list of users.\n\n"
        "**Example:** `GET /api/v1/users?skip=0&limit=10`"
    ),
)
def list_users(
    skip: int = Query(
        0,
        ge=0,
        description="Number of records to skip",
    ),
    limit: int = Query(
        100,
        ge=1,
        le=200,
        description="Maximum number of records to return",
    ),
    db: Session = Depends(get_db),
):
    """
    Retrieve paginated users.
    """

    total, users = user_service.get_all_users(
        db=db,
        skip=skip,
        limit=limit,
    )

    return {
        "total": total,
        "users": users,
    }


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    description=(
        "Retrieve a specific user by UUID.\n\n"
        "**Example:** "
        "`GET /api/v1/users/3fa85f64-5717-4562-b3fc-2c963f66afa6`"
    ),
    responses={
        404: {"description": "User not found"},
    },
)
def get_user(
    user_id: str,
    db: Session = Depends(get_db),
):
    """
    Retrieve a single user by ID.
    """

    return user_service.get_user_by_id(db, user_id)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create user",
    description=(
        "Create a new user.\n\n"
        "**Example request body:**\n"
        "```json\n"
        "{\n"
        '  "username": "gseguel",\n'
        '  "email": "gseguel@example.com",\n'
        '  "first_name": "Gustavo",\n'
        '  "last_name": "Seguel",\n'
        '  "role": "user",\n'
        '  "active": true\n'
        "}\n"
        "```"
    ),
    responses={
        409: {"description": "Username or email already exists"},
    },
)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new user.
    """

    return user_service.create_user(db, data)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update user",
    description=(
        "Partially update an existing user.\n\n"
        '**Example request body:** `{"active": false}`'
    ),
    responses={
        404: {"description": "User not found"},
        409: {"description": "Username or email already exists"},
    },
)
def update_user(
    user_id: str,
    data: UserUpdate,
    db: Session = Depends(get_db),
):
    """
    Partially update a user.
    """

    return user_service.update_user(db, user_id, data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete user",
    description=(
        "Permanently delete a user.\n\n"
        "**Example:** "
        "`DELETE /api/v1/users/3fa85f64-5717-4562-b3fc-2c963f66afa6`"
    ),
    responses={
        404: {"description": "User not found"},
    },
)
def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
):
    """
    Delete a user by ID.
    """

    return user_service.delete_user(db, user_id)