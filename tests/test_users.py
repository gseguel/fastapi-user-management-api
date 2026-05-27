"""
User API integration tests.

Test database setup and dependency overrides
are defined in conftest.py.
"""

# Default payload used across tests
VALID_USER = {
    "username": "gseguel",
    "email": "gseguel@example.com",
    "first_name": "Gustavo",
    "last_name": "Seguel",
    "role": "user",
    "active": True,
}


def create_user(client, payload=None):
    """Helper to create a user."""

    return client.post(
        "/api/v1/users/",
        json=payload or VALID_USER,
    )


# ──────────────────────────────────────────────────────────────────────────────
# Health check
# ──────────────────────────────────────────────────────────────────────────────
def test_health_check(client):
    """Check health endpoint."""

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# ──────────────────────────────────────────────────────────────────────────────
# Create user
# ──────────────────────────────────────────────────────────────────────────────
def test_create_user_success(client):
    """Create user successfully."""

    response = create_user(client)

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "gseguel"
    assert data["email"] == "gseguel@example.com"
    assert "id" in data
    assert "created_at" in data


def test_create_user_duplicate_username(client):
    """Reject duplicate usernames."""

    create_user(client)

    response = create_user(client)

    assert response.status_code == 409
    assert "username" in response.json()["detail"].lower()


def test_create_user_duplicate_email(client):
    """Reject duplicate emails."""

    create_user(client)

    response = create_user(
        client,
        payload={
            **VALID_USER,
            "username": "anotheruser",
        },
    )

    assert response.status_code == 409
    assert "email" in response.json()["detail"].lower()


def test_create_user_invalid_email(client):
    """Validate invalid email format."""

    response = create_user(
        client,
        payload={
            **VALID_USER,
            "email": "invalid-email",
        },
    )

    assert response.status_code == 422


def test_create_user_invalid_role(client):
    """Validate unsupported roles."""

    response = create_user(
        client,
        payload={
            **VALID_USER,
            "role": "superadmin",
        },
    )

    assert response.status_code == 422


def test_create_user_short_username(client):
    """Validate minimum username length."""

    response = create_user(
        client,
        payload={
            **VALID_USER,
            "username": "ab",
        },
    )

    assert response.status_code == 422


def test_create_user_username_with_spaces(client):
    """Reject usernames with spaces."""

    response = create_user(
        client,
        payload={
            **VALID_USER,
            "username": "gustavo seguel",
        },
    )

    assert response.status_code == 422


def test_create_user_username_starts_with_hyphen(client):
    """Reject usernames starting with hyphen."""

    response = create_user(
        client,
        payload={
            **VALID_USER,
            "username": "-gseguel",
        },
    )

    assert response.status_code == 422


# ──────────────────────────────────────────────────────────────────────────────
# Read user
# ──────────────────────────────────────────────────────────────────────────────
def test_get_user_success(client):
    """Get an existing user."""

    user_id = create_user(client).json()["id"]

    response = client.get(f"/api/v1/users/{user_id}")

    assert response.status_code == 200
    assert response.json()["id"] == user_id


def test_get_user_not_found(client):
    """Return 404 when user does not exist."""

    response = client.get("/api/v1/users/non-existent-id")

    assert response.status_code == 404


def test_list_users_empty(client):
    """Return empty list when no users exist."""

    response = client.get("/api/v1/users/")

    assert response.status_code == 200
    assert response.json() == {
        "total": 0,
        "users": [],
    }


def test_list_users_with_data(client):
    """Return users when data exists."""

    create_user(client)

    create_user(
        client,
        payload={
            **VALID_USER,
            "username": "seconduser",
            "email": "second@example.com",
        },
    )

    response = client.get("/api/v1/users/")

    assert response.status_code == 200
    assert response.json()["total"] == 2


def test_list_users_pagination(client):
    """Validate pagination."""

    for i in range(5):
        create_user(
            client,
            payload={
                **VALID_USER,
                "username": f"user{i}",
                "email": f"user{i}@example.com",
            },
        )

    response = client.get("/api/v1/users/?skip=2&limit=2")

    assert response.status_code == 200
    assert len(response.json()["users"]) == 2
    assert response.json()["total"] == 5


# ──────────────────────────────────────────────────────────────────────────────
# Update user
# ──────────────────────────────────────────────────────────────────────────────
def test_update_user_success(client):
    """Update user fields."""

    user_id = create_user(client).json()["id"]

    response = client.patch(
        f"/api/v1/users/{user_id}",
        json={
            "first_name": "Updated",
            "active": False,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["first_name"] == "Updated"
    assert data["active"] is False


def test_update_user_role(client):
    """Update user role."""

    user_id = create_user(client).json()["id"]

    response = client.patch(
        f"/api/v1/users/{user_id}",
        json={"role": "admin"},
    )

    assert response.status_code == 200
    assert response.json()["role"] == "admin"


def test_update_user_not_found(client):
    """Return 404 when updating missing user."""

    response = client.patch(
        "/api/v1/users/non-existent-id",
        json={"active": False},
    )

    assert response.status_code == 404


def test_update_user_duplicate_username(client):
    """Reject duplicate username on update."""

    create_user(client)

    second_user_id = create_user(
        client,
        payload={
            **VALID_USER,
            "username": "anotheruser",
            "email": "another@example.com",
        },
    ).json()["id"]

    response = client.patch(
        f"/api/v1/users/{second_user_id}",
        json={"username": "gseguel"},
    )

    assert response.status_code == 409


# ──────────────────────────────────────────────────────────────────────────────
# Delete user
# ──────────────────────────────────────────────────────────────────────────────
def test_delete_user_success(client):
    """Delete user successfully."""

    user_id = create_user(client).json()["id"]

    response = client.delete(f"/api/v1/users/{user_id}")

    assert response.status_code == 200

    get_response = client.get(f"/api/v1/users/{user_id}")

    assert get_response.status_code == 404


def test_delete_user_not_found(client):
    """Return 404 when deleting missing user."""

    response = client.delete("/api/v1/users/non-existent-id")

    assert response.status_code == 404