from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseMode(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


# class TypeUser(BaseMode):
#     type_user = models.CharField(max_length=128)
#
#     def __str__(self):
#         return f'{self.type_user}'

class ApiUser(AbstractUser):
    type_user = models.CharField(max_length=128)


class Storage(BaseMode):
    name = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.name}'


class Product(BaseMode):
    name = models.CharField(max_length=128)
    price = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()
    storage = models.ForeignKey(Storage, related_name="products", on_delete=models.CASCADE)

    def __str__(self):
        return f'Storage: {self.storage}. Product: {self.name}. Amount: {self.amount}'


class Order(BaseMode):
    storage = models.ForeignKey(Storage, related_name='order', on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now())
    product = models.ForeignKey(Product, related_name='product', on_delete=models.CASCADE)
    type_order = models.CharField(max_length=128)
    amount_product = models.IntegerField()

    def __str__(self):
        return f'Id of order. Storage: {self.storage}. Product{self.product.name}'
