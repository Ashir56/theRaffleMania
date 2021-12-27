from django.db import models
from .core import UserModels, CardModel, GenericModels, CartModel
# Create your models here.


class Buyer(UserModels):
    uid = models.CharField(max_length=100, primary_key=True, unique=True)
    userName = models.CharField(max_length=100)
    email = models.EmailField()
    profile_pic = models.ImageField(null=True)
    gender = models.CharField(max_length=10)
    dob = models.DateField(max_length=10)
    phoneNumber = models.CharField(max_length=50)
    address = models.TextField(max_length=150)


class Billing(GenericModels):
    instance = models.ForeignKey(Buyer, on_delete=models.SET_NULL, null=True)
    total = models.IntegerField(max_length=5, null=True)
    discount = models.IntegerField(max_length=5, null=True)
    shipping_fee = models.IntegerField(max_length=5, null=True)
    tax = models.IntegerField(max_length=5, null=True)
    grand_total = models.IntegerField(max_length=10, null=True)
    product_size = models.IntegerField(default=0)


class BuyerCard(CardModel):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, unique=True)


class Cart(CartModel):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='Buyer')
    product = models.ForeignKey('Product.Products', on_delete=models.CASCADE, null=True, related_name='Product')
    name = models.CharField(max_length=100)
