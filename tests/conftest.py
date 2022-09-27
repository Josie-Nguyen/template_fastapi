from http import client
from pyexpat import model
import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydoc import cli
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.oauth2 import create_access_token
from app import models
from app.database import get_db, Base



SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
#SQLALCHEMY_DATABASE_URL = "postgresql://<user_name>:<password>@<ip_address/hostname>/<database_name>"


engine = create_engine( SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base.metadata.create_all(bind=engine)

# Dependency
# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# app.dependency_overrides[get_db] = override_get_db
# client = TestClient(app)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email":"test123@gmail.com", "password": "testne123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def test_user1(client):
    user_data = {"email":"josie.ng@gmail.com", "password": "testne123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client,token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_post(test_user, session, test_user1):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    },{
        "title": "second title",
        "content": "second content",
        "owner_id": test_user['id']
    },{
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user1['id']
    }]

    def create_post_model(post):
        return models.Post(**post)
    post_map = map(create_post_model, posts_data)
    posts = list(post_map)


    session.add_all(posts)
        # [models.Post(title= "first title", content= "first content", id= test_user['id']),
        #                 models.Post(title = "second title", content = "second content", id = test_user['id']),
        #                 models.Post(title = "3rd title",content = "3rd content",id = test_user['id'])])
    session.commit()
    posts = session.query(models.Post).all()
    return posts