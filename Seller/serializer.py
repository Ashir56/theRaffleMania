from rest_framework.serializers import ModelSerializer
from .models import Seller
import stripe
import re
from RaffleMania.settings import STRIPE_SECRET_KEY
stripe.api_key = STRIPE_SECRET_KEY


class SellerSerializer(ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'
        read_only_fields = ('usermodels_ptr', 'cardmodel_ptr',)

    def validate(self, data):
        buyer = data.get('buyer')
        data['seller_id'] = buyer.uid
        expiryDate = data.get('expiryDate')
        expiryDate = expiryDate.strftime('%Y-%m-%d')
        exp_year = re.split('-', expiryDate)

        token = stripe.Token.create(
            card={
                "number": data.get('cardNumber'),
                "exp_month": exp_year[1],
                "exp_year": exp_year[0],
                "cvc": data.get('cvcNum'),
            },
        )

        customer = stripe.Customer.create(
            source=token,
            description="My First Test Customer (created for API docs)",
        )
        data['token'] = customer.stripe_id

        return data
