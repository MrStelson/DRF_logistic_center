import pytest

from api.serializers import UserSerializer
from api.models import ApiUser, Storage, Product


@pytest.fixture
def user_provider():
    user = ApiUser.objects.create(
        username="test_user_provider",
        email="test_provider@email.com",
        type_user="provider"
    )

    user.set_password("123123")
    user.save(update_fields=['password'])

    return user


@pytest.fixture
def user_consumer():
    user = ApiUser.objects.create(
        username="test_user_consumer",
        email="test_consumer@email.com",
        type_user="consumer"
    )

    user.set_password("123123")
    user.save(update_fields=['password'])

    return user


@pytest.fixture
def storage():
    storage = Storage.objects.create(name="test_storage")
    storage.save()
    return storage


@pytest.fixture
def product(storage):
    product = Product.objects.create(
        name="test_product",
        price=1,
        amount=10,
        storage=storage
    )
    product.save()
    return product
