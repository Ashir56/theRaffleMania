from django.contrib import admin
from .models import Buyer, Cart, BuyerCard, Billing
# Register your models here.

admin.site.register(Buyer)
admin.site.register(Cart)
admin.site.register(BuyerCard)
admin.site.register(Billing)
