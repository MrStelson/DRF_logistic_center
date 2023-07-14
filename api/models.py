from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class ApiUser(AbstractUser):
    type_user = models.CharField(max_length=128)


class Storage(models.Model):
    name = models.CharField(max_length=128)


class Product(models.Model):
    name = models.CharField(max_length=128)
    price = models.PositiveIntegerField()
    storage = models.ForeignKey(Storage, related_name="products", on_delete=models.CASCADE)
