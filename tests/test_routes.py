import pytest
from app.logger import logger
import random

# from .main import app
from app.main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_get_gigi(client):
    response = client.get("/gigi")
    assert response.status_code == 200
    assert response.data.decode() == "this is gigi"


user_data_signup = {
    # "name": f"ion{random.randint(100, 999)}",
    "name": "awdadw90909",
    "password": "gigi123A",
    "confirm_password": "gigi123A",
    # "email": f"fe{random.randint(100, 999)}@gmail.com",
    "email": "awdadw908h0@gmail.com",
}


def test_signup(client):
    response = client.post("/signup", json=user_data_signup)
    assert response.status_code == 201
    assert response.get_json() == f"User created with email {user_data_signup['name']}"


# user_data_login = {
#     "name": user_data_signup["name"],
#     "password": "gigi123A",
# }


# def test_signin(client):
#     response = client.post("/login", data=user_data_login)
#     assert response.status_code == 200
#     access_token = response.get_json()["access_token"]
#     logger.info(access_token)
#     assert access_token.startswith("ey")
