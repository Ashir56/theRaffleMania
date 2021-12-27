from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from .serializer import BuyerSerializer, BuyerCardSerializer, BillingSerializer, \
    CartSerializer, BuyerCardUpdateSerializer, AddressSerializer
from .models import Buyer, BuyerCard, Billing, Cart
from rest_framework.generics import GenericAPIView
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, \
    UpdateModelMixin, DestroyModelMixin
from rest_framework.decorators import action
from Product.models import ProductBuyer
import stripe
from django.core.mail import send_mail
from RaffleMania.settings import STRIPE_SECRET_KEY
from RaffleMania import settings
stripe.api_key = STRIPE_SECRET_KEY


# Create your views here.


def home(request):
    return HttpResponse('<h1>BLOGS</h1>')


class BuyerAPI(GenericAPIView):
    serializer_class = BuyerSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response({"success": True, "Msg": "Buyer Created Successfully"},
                            status=status.HTTP_201_CREATED)
        return Response({"success": False, "Msg": str(self.serializer_class.errors)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            buyer_id = request.headers.get('Authorization')
            buyer = Buyer.objects.get(uid=buyer_id)
            serializer = BuyerSerializer(buyer)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response({"success": False, "Msg": "User Does Not Exist"},
                            status=status.HTTP_200_OK)

    def patch(self, request):
        try:
            buyer_id = request.headers.get('Authorization')
            buyer = Buyer.objects.get(uid=buyer_id)
            serializer = BuyerSerializer(buyer, data=self.request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
            return Response({"success": True, "msg": "User Updated"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        try:
            buyer_id = request.headers.get('Authorization')
            buyer = Buyer.objects.get(uid=buyer_id)
            buyer.delete()
            return Response({"success": True, "msg": "Buyer Deleted"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BuyerCardAPI(viewsets.GenericViewSet, CreateModelMixin,
                   RetrieveModelMixin, DestroyModelMixin):
    serializer_class = BuyerCardSerializer
    model = BuyerCard
    lookup_field = 'buyer_id'
    queryset = BuyerCard.objects.all()

    def get_queryset(self):
        buyer_id = self.request.headers.get('Authorization')
        qs = BuyerCard.objects.get(buyer_id=buyer_id)
        return qs

    def get_object(self):
        object = self.get_queryset()
        return object

    @action(methods=['post'], detail=True)
    def post(self, request, *args, **kwargs):
        try:
            self.create(request, *args, **kwargs)
            return Response({"success": True, "msg": "Card Added"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['get'], detail=True)
    def get(self, request, *args, **kwargs):
        try:
            return self.retrieve(request, *args, **kwargs)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": "Card Does Not Exist"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['delete'], detail=True)
    def delete(self, request, *args, **kwargs):
        try:
            self.destroy(request, *args, **kwargs)
            return Response({"success": True, "msg": "Card Deleted"},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)
            return Response({"success": False, "mdg": "Card does not exist"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['patch'], detail=True)
    def patch(self, request):
        self.serializer_class = BuyerCardUpdateSerializer
        try:
            obj = self.get_object()
            serializer = self.serializer_class(obj, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"success": True, "msg": "Card Data is Updated"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BuyerCartAPI(viewsets.ModelViewSet, CreateModelMixin):
    model = Cart
    lookup_field = 'buyer_id'
    serializer_class = CartSerializer

    def get_queryset(self):
        buyer_id = self.request.headers.get('Authorization')
        qs = Cart.objects.filter(buyer_id=buyer_id)
        return qs

    def get_object(self):
        obj = self.get_queryset()
        return obj

    @action(methods=['post'], detail=True)
    def post(self, request, *args, **kwargs):
        if self.create(request, *args, **kwargs):
            return Response({"success": True, "msg": "Product Added to Cart"},
                            status=status.HTTP_201_CREATED)
        return Response({"success": False, "msg": self.serializer_class.errors},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['delete'], detail=True)
    def delete(self, request):
        try:
            user_id = request.headers.get('Authorization')
            user = Buyer.objects.get(uid=user_id)
            carts = Cart.objects.filter(buyer=user)
            if carts.exists():
                for cart in carts:
                    product = cart.product
                    product.ticket_limit += cart.number_of_tickets
                    product.save()
                carts.delete()
            return Response({"success": True, "msg": "Cart Deleted"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": "User Does Not Exist"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, *kwargs)


class BillingAPI(GenericAPIView):
    # Billing Creation and Cart Deletion
    def post(self, request):
        try:
            user_id = request.data.get('user_id')
            shipping_fee = request.data.get('fee')
            user = Buyer.objects.get(user_id=user_id)
            # Get User Cart
            carts = Cart.objects.filter(buyer=user)
            discount = request.data.get('discount')
            # Get User Credit Card
            card = BuyerCard.objects.get(association=user)
            print(carts)

            if not carts:
                raise Exception('There is nothing to buy')

            if not user:
                raise Exception('There is no user of this type')

            if not card:
                raise Exception('You do not have a credit card Registered')

            for cart in carts:
                product = cart.product
                number_of_tickets = cart.number_of_tickets
                buyer = ProductBuyer.objects.create(buyer=user, product=product, number_of_tickets=number_of_tickets)

            if discount is None:
                discount = 0
            prices = []
            for cart in carts:
                price = cart.product.ticket_price

                product = cart.product
                # Update Product Ticket Sold
                product.ticket_sold += cart.number_of_tickets
                price *= cart.number_of_tickets
                product.save()
                prices.append(price)
            total_sum = sum(prices)
            total = total_sum + int(shipping_fee)
            grand_total = total-int(discount)
            tax = (grand_total*1)/100
            grand_total += tax
            grand_total = int(grand_total)
            stripe.Charge.create(
                amount=grand_total * 100,
                currency="usd",
                customer=card.token,
                description="My First Test Charge (created for API docs)",
            )
            # Delete User Cart
            carts.delete()
            billing = Billing.objects.create(instance=user, shipping_fee=shipping_fee, tax=tax,
                                             grand_total=grand_total, total=total_sum, discount=discount)
            return Response({"success": True, "msg": str(billing)}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            user_id = request.headers.get('Authorization')
            user = Buyer.objects.get(user_id=user_id)
            bills = Billing.objects.filter(instance=user)
            serializer = []
            for bill in bills:
                ser = BillingSerializer(bill, many=True)
                serializer.append(ser.data)

            return Response(serializer, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class getAddress(GenericAPIView):
    #GET ADDRESS
    def get(self, request):
        try:
            fields = ('username', 'address', 'phoneNumber')
            user_id = request.headers.get('Authorization')
            user = Buyer.objects.get(uid=user_id)
            serializer = AddressSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SendEmailAPI(GenericAPIView):
    def post(self, request):
        send_mail(
            subject=request.data.get('Subject'),
            message=request.data.get('message'),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[request.data.get('receiver')]

        )
        return Response({"success": True}, status=status.HTTP_200_OK)
