def test_register_success(client):
    # Act
    response = client.post(
        "/api/v1/auth/register",
        json={"login": "newuser", "password": "secret123"}
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["login"] == "newuser"
    assert "id" in response.json()
    assert "password" not in response.json()


def test_register_duplicate(client):
    # Arrange — создаём пользователя первый раз
    client.post("/api/v1/auth/register", json={"login": "newuser", "password": "secret123"})

    # Act — пытаемся создать того же пользователя снова
    response = client.post(
        "/api/v1/auth/register",
        json={"login": "newuser", "password": "secret123"}
    )

    # Assert
    assert response.status_code == 400


def test_register_short_password(client):
    # Act
    response = client.post(
        "/api/v1/auth/register",
        json={"login": "newuser", "password": "123"}
    )

    # Assert
    assert response.status_code == 422


def test_login_success(client):
    # Arrange
    client.post("/api/v1/auth/register", json={"login": "newuser", "password": "secret123"})

    # Act
    response = client.post(
        "/api/v1/auth/login",
        json={"login": "newuser", "password": "secret123"}
    )

    # Assert
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_wrong_password(client):
    # Arrange
    client.post("/api/v1/auth/register", json={"login": "newuser", "password": "secret123"})

    # Act
    response = client.post(
        "/api/v1/auth/login",
        json={"login": "newuser", "password": "wrongpassword"}
    )

    # Assert
    assert response.status_code == 401


def test_login_not_existing_user(client):
    # Act
    response = client.post(
        "/api/v1/auth/login",
        json={"login": "ghost", "password": "secret123"}
    )

    # Assert
    assert response.status_code == 401


def test_get_me_success(client, auth_headers):
    # Act
    response = client.get("/api/v1/users/me", headers=auth_headers)

    # Assert
    assert response.status_code == 200
    assert response.json()["login"] == "testuser"


def test_get_me_unauthorized(client):
    # Act
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer invalidtoken"}
    )

    # Assert
    assert response.status_code == 401