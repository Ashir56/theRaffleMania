from django.db import models
from Buyer.core import GenericModels, CartModel
from Buyer.models import Buyer

# Create your models here.


class Products(GenericModels):
    product_id = models.IntegerField(auto_created=True, primary_key=True, unique=True)
    instance = models.ForeignKey('Seller.Seller', on_delete=models.CASCADE)
    productName = models.CharField(max_length=50, null=True)
    shortDesc = models.CharField(max_length=150, null=True)
    product_status = models.BooleanField(default=False, max_length=1)
    detailDesc = models.CharField(max_length=350, null=True)
    product_price = models.IntegerField(null=True)
    ticket_price = models.IntegerField(null=True)
    raffleTime = models.TimeField(null=True)
    category = models.CharField(max_length=100, null=True)
    ticket_limit = models.IntegerField()
    ticket_sold = models.IntegerField(default=0)
    product_size = models.JSONField(null=True)
    product_rating = models.DecimalField(decimal_places=1, max_digits=2, default=0.0)
    product_image1 = models.ImageField(null=True, upload_to='Product/Images')
    product_image2 = models.ImageField(null=True, upload_to='Product/Images')
    product_image3 = models.ImageField(null=True, upload_to='Product/Images')
    product_image4 = models.ImageField(null=True, upload_to='Product/Images')
    product_image5 = models.ImageField(null=True, upload_to='Product/Images')
    product_image6 = models.ImageField(null=True, upload_to='Product/Images')
    product_image7 = models.ImageField(null=True, upload_to='Product/Images')
    product_image8 = models.ImageField(null=True, upload_to='Product/Images')
    product_image9 = models.ImageField(null=True, upload_to='Product/Images')
    product_image10 = models.ImageField(null=True, upload_to='Product/Images')
    product_imageList = models.JSONField(null=True)


class Wishlist(GenericModels):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)


class Order(GenericModels):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    order_dispatched = models.BooleanField(default=False)
    in_way = models.BooleanField(default=False)
    order_delivered = models.BooleanField(default=False)


class Reviews(GenericModels):
    instance = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    review = models.TextField(max_length=250, null=True)
    rating = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)


class ProductBuyer(CartModel):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
