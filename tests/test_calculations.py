import pytest

def _seed_user(client):
    client.post("/users/register", json={
        "email": "tester@example.com", "username": "tester", "password": "pass"
    })

def test_add_calculation(client):
    _seed_user(client)
    r = client.post("/calculations/", json={
        "operation": "add", "operand_a": 10, "operand_b": 5
    })
    assert r.status_code == 201
    assert r.json()["result"] == 15.0

def test_browse_calculations(client):
    r = client.get("/calculations/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_read_calculation(client):
    created = client.post("/calculations/", json={
        "operation": "multiply", "operand_a": 3, "operand_b": 4
    }).json()
    r = client.get(f"/calculations/{created['id']}")
    assert r.status_code == 200
    assert r.json()["result"] == 12.0

def test_edit_calculation(client):
    created = client.post("/calculations/", json={
        "operation": "add", "operand_a": 1, "operand_b": 1
    }).json()
    r = client.patch(f"/calculations/{created['id']}", json={"operand_a": 10})
    assert r.status_code == 200
    assert r.json()["result"] == 11.0

def test_delete_calculation(client):
    created = client.post("/calculations/", json={
        "operation": "subtract", "operand_a": 9, "operand_b": 3
    }).json()
    r = client.delete(f"/calculations/{created['id']}")
    assert r.status_code == 204
    r2 = client.get(f"/calculations/{created['id']}")
    assert r2.status_code == 404

def test_divide_by_zero(client):
    r = client.post("/calculations/", json={
        "operation": "divide", "operand_a": 5, "operand_b": 0
    })
    assert r.status_code == 422

def test_invalid_operation(client):
    r = client.post("/calculations/", json={
        "operation": "modulo", "operand_a": 5, "operand_b": 2
    })
    assert r.status_code == 422