from django.contrib import admin
from .models import Products, ProductBuyer, Reviews, Order, Wishlist
# Register your models here.

admin.site.register(Products)
admin.site.register(ProductBuyer)
admin.site.register(Reviews)
admin.site.register(Order)
admin.site.register(Wishlist)
