import pytest
from rest_framework.test import APIClient
from rest_framework import serializers

client = APIClient()


@pytest.mark.django_db
def test_user_in_db(user_provider):
    response = client.get("/users/")
    data = response.data
    assert data[0]['username'] == "test_user_provider"


@pytest.mark.django_db
def test_user_create():
    payload = dict(
        username="test_user",
        email="test@emal.com",
        password="123123",
        type_user="provider"
    )

    response = client.post("/users/", payload)
    data = response.data
    assert data['username'] == payload['username']
    assert data['email'] == payload['email']
    assert data['type_user'] == payload['type_user']
    assert "password" not in data


@pytest.mark.django_db
def test_user_create_wrong_type():
    payload = dict(
        username="test_user",
        email="test@emal.com",
        password="123123",
        type_user="new_type"
    )

    client.post("/users/", payload)
    assert serializers.ValidationError("Type user must be provider or consumer")


@pytest.mark.django_db
def test_user_login(user_provider):
    response = client.post("/api-token-auth/", dict(username="test_user_provider", password="123123"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_storage_without_auth():
    response = client.post("/storages/", dict(name="test_storage"))
    data = response.data
    assert data["detail"] == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_create_storage(user_provider):
    client.login(username='test_user_provider', password='123123')
    response = client.post("/storages/", dict(name="test_storage"))
    data = response.data
    assert data['name'] == "test_storage"


@pytest.mark.django_db
def test_get_storage(storage):
    response = client.get("/storages/")
    data = response.data
    assert data[0]['name'] == 'test_storage'


@pytest.mark.django_db
def test_create_product_fail(storage):
    payload = dict(
        name="test_product",
        price=5,
        amount=10,
        storage=1
    )
    response = client.post("/products/", payload)
    data = response.data
    assert data["detail"] == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_create_product(storage, user_provider):
    payload = dict(
        name="test_product",
        price=5,
        amount=10,
        storage=1
    )
    client.login(username='test_user_provider', password='123123')
    response = client.post("/products/", payload)
    data = response.data
    assert response.status_code == 201
    assert data['name'] == payload['name']
    assert data['price'] == payload['price']
    assert data['amount'] == payload['amount']


@pytest.mark.django_db
def test_create_order_supply(user_provider, storage, product):
    payload = dict(
        amount_product=5,
        storage=1,
        product=1
    )
    client.login(username='test_user_provider', password='123123')
    response = client.post("/order/", payload)
    product.amount += payload['amount_product']
    data = response.data
    assert data['type_order'] == 'supply'
    assert product.amount == 15


@pytest.mark.django_db
def test_create_order_sending(user_consumer, storage, product):
    payload = dict(
        amount_product=5,
        storage=1,
        product=1
    )
    client.login(username='test_user_consumer', password='123123')
    response = client.post("/order/", payload)
    product.amount -= payload['amount_product']
    data = response.data
    assert data['type_order'] == 'sending'
    assert product.amount == 5
