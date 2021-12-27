from django.db import models
from Buyer.models import Buyer
from Buyer.core import CardModel
# Create your models here.


class Seller(CardModel):
    seller_id = models.CharField(max_length=1000, primary_key=True, default=None)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, unique=True)
    abn = models.BigIntegerField()
    package = models.IntegerField()
