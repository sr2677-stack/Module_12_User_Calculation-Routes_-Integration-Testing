def test_register_success(client):
    r = client.post("/users/register", json={
        "email": "alice@example.com",
        "username": "alice",
        "password": "secret123"
    })
    assert r.status_code == 201
    data = r.json()
    assert data["email"] == "alice@example.com"
    assert "hashed_pw" not in data          # password never exposed

def test_register_duplicate_email(client):
    payload = {"email": "bob@example.com", "username": "bob", "password": "pass"}
    client.post("/users/register", json=payload)
    r = client.post("/users/register", json=payload)
    assert r.status_code == 400

def test_login_success(client):
    client.post("/users/register", json={
        "email": "carol@example.com", "username": "carol", "password": "mypass"
    })
    r = client.post("/users/login", json={
        "email": "carol@example.com", "password": "mypass"
    })
    assert r.status_code == 200
    assert "access_token" in r.json()

def test_login_wrong_password(client):
    client.post("/users/register", json={
        "email": "dave@example.com", "username": "dave", "password": "correct"
    })
    r = client.post("/users/login", json={
        "email": "dave@example.com", "password": "wrong"
    })
    assert r.status_code == 401