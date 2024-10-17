import pytest
from fastapi.testclient import TestClient
from app.main import main

client = TestClient

def test_register_user():
    response = client.post('/register', json={
        'username': 'Marc Gilbert Lim',
        'password': 'password123!',
        'email': 'adminuser@gmail.com',
        'role': 'admin'
    })
    assert response.status_code == 200