from rest_framework.serializers import ModelSerializer
from Buyer.models import Buyer, BuyerCard, Billing, Cart
import re
import stripe
from RaffleMania.settings import STRIPE_SECRET_KEY
stripe.api_key = STRIPE_SECRET_KEY


class BuyerSerializer(ModelSerializer):

    class Meta:
        model = Buyer
        read_only_fields = ('usermodels_ptr',)
        fields = '__all__'


class BuyerCardSerializer(ModelSerializer):

    class Meta:
        model = BuyerCard
        read_only_fields = ('cardmodel_ptr',)
        fields = '__all__'

    def validate(self, data):
        expiryDate = data.get('expiryDate')
        if data.get('cardName') is None:
            raise ValueError("Card Name is required")
        if data.get('cardNumber') is None:
            raise ValueError("Card Number is required")
        if data.get('expiryDate') is None:
            raise ValueError("Expiry Date is required")
        if data.get('cvcNum') is None:
            raise ValueError("CVC num is required")

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


class BuyerCardUpdateSerializer(ModelSerializer):
    class Meta:
        model = BuyerCard
        fields = '__all__'
        read_only_fields = ('cardmodel_ptr',)


class BillingSerializer(ModelSerializer):

    class Meta:
        model = Billing
        read_only_fields = ('genericmodels_ptr',)
        fields = '__all__'


class CartSerializer(ModelSerializer):

    class Meta:
        model = Cart
        read_only_fields = ('cartmodel_ptr',)
        fields = '__all__'

    def validate(self, data):
        buyer = data.get('buyer')
        product = data.get('product')
        number_of_tickets = data.get('number_of_tickets')
        if buyer is None:
            raise ValueError("This Buyer Does Not Exist")
        if product is None:
            raise ValueError("This Product Does Not Exist")
        if number_of_tickets > product.ticket_limit:
            raise ValueError("Ticket Limit Exceeded")

        product.ticket_limit -= number_of_tickets
        product.save()
        return data


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Buyer
        fields = ['username', 'address', 'phoneNumber']
