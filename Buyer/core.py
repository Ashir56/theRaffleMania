from django.db import models


class GenericModels(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)


class UserModels(GenericModels):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)


class CardModel(GenericModels):
    token = models.CharField(max_length=100, null=True)
    cardName = models.CharField(max_length=100, null=True)
    cardNumber = models.BigIntegerField(max_length=100, null=True)
    expiryDate = models.DateField(null=True)
    cvcNum = models.IntegerField(max_length=10, null=True)


class CartModel(GenericModels):
    product_size = models.IntegerField(default=0)
    number_of_tickets = models.IntegerField(default=1)

