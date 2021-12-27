from .models import Products, ProductBuyer, Wishlist, Order, Reviews
from .serializer import ProductsSerializer, ProductBuyerSerializer, ReviewsSerializer, \
    OrderSerializer, WishlistSerializer
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, \
    DestroyModelMixin, ListModelMixin
from Seller.models import Seller
from Buyer.models import Buyer
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction


class ProductAPI(viewsets.GenericViewSet, CreateModelMixin,
                 RetrieveModelMixin, DestroyModelMixin):
    serializer_class = ProductsSerializer
    model = Products
    lookup_field = 'instance'
    queryset = Products.objects.all()

    def get_queryset(self):
        instance = self.request.headers.get('Authorization')
        seller = Seller.objects.get(seller_id=instance)
        qs = Products.objects.get(instance=seller)
        print(qs)
        return qs

    def get_object(self):
        object_id = self.get_queryset()
        return object_id

    @action(methods=['post'], detail=True)
    def post(self, request, *args, **kwargs):
        try:
            request.data['product_size'] = [request.data.get('product_size')]
            self.create(request, *args, **kwargs)
            return Response({"success": True, "msg": "Product Added"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['get'], detail=True)
    def get(self, request, *args, **kwargs):
        try:
            instance = self.request.headers.get('Authorization')
            seller = Seller.objects.get(seller_id=instance)
            qs = Products.objects.filter(instance=seller)
            serializer = ProductsSerializer(qs, many=True)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": "Product Does Not Exist"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['delete'], detail=True)
    def delete(self, request, *args, **kwargs):
        try:
            self.destroy(request, *args, **kwargs)
            return Response({"success": True, "msg": "Product Deleted"},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)
            return Response({"success": False, "mdg": "Product does not exist"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['patch'], detail=True)
    def patch(self, request):
        try:
            obj = self.get_object()
            serializer = self.serializer_class(obj, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"success": True, "msg": "Product Data is Updated"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductBuyerAPI(viewsets.GenericViewSet):
    serializer_class = ProductBuyerSerializer
    model = ProductBuyer
    queryset = ProductBuyer.objects.all()


class ReviewAPI(GenericAPIView):
    serializer_class = ReviewsSerializer
    model = Reviews
    queryset = Reviews.objects.all()

    def get_queryset(self):
        product_id = self.request.headers.get('Authorization')
        product = Products.objects.get(product_id=product_id)
        reviews = Reviews.objects.filter(product=product).values()
        return reviews

    def get_object(self):
        reviews = self.get_queryset()
        return reviews

    @action(methods=['post'], detail=True)
    def post(self, request):
        try:
            product_id = request.data.get('product')
            product = Products.objects.get(product_id=product_id)
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            reviews = Reviews.objects.filter(product=product).values()
            rating = []
            for review in reviews:
                rate = review['rating']
                rating.append(rate)
                size = len(rating)
                Sum = sum(rating)
                product_rating = Sum / size
                product.product_rating = product_rating
                product.save()
            return Response({"success": True, "msg": "Review Added"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['get'], detail=True)
    def get(self, request):
        try:
            product_id = self.request.headers.get('Authorization')
            product = Products.objects.get(product_id=product_id)
            reviews = Reviews.objects.filter(product=product).values()
            serializer = ReviewsSerializer(reviews, many=True)
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": "There are no reviews for this"})


class WishlistAPI(viewsets.GenericViewSet, CreateModelMixin,
                  RetrieveModelMixin, ListModelMixin):
    serializer_class = WishlistSerializer
    model = Wishlist
    queryset = Wishlist.objects.all()

    def get_buyer(self):
        buyer_id = self.request.headers.get('Authorization')
        qs = Buyer.objects.get(uid=buyer_id)
        return qs

    def get_queryset(self):
        buyer_id = self.request.headers.get('Authorization')
        qs = Buyer.objects.get(uid=buyer_id)
        wishlist = Wishlist.objects.filter(buyer=qs)
        return wishlist

    def get_object(self):
        object = self.get_queryset()
        print(object)
        return object

    @action(methods=['post'], detail=True)
    def post(self, request, *args, **kwargs):
        try:
            self.create(request, *args, **kwargs)
            return Response({"success": True, "Msg": "Product Added to Wishlist"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"success": False, "Msg": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['get'], detail=True)
    def get(self, request, *args, **kwargs):
        try:
            return self.list(request, *args, **kwargs)
        except Exception as e:
            print(e)
            return Response({"success": False, "Msg": "User Does Not Exist"},
                            status=status.HTTP_200_OK)

    @action(methods=['delete'], detail=True)
    def delete(self, request):
        try:
            buyer_id = request.headers.get('Authorization')
            buyer = Buyer.objects.get(uid=buyer_id)
            product_id = request.GET.get('product_id')
            product = Products.objects.get(product_id=product_id)
            wishlist = Wishlist.objects.get(buyer=buyer, product=product)
            wishlist.delete()
            return Response({"success": True, "msg": "Product Deleted From wishlist"},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductByPrice(GenericAPIView):
    def get(self, request):
        try:
            category = request.GET.get('category')
            mini = request.GET.get('min')
            maxi = request.GET.get('max')
            if category and mini and maxi:
                products = Products.objects.filter(category=category).values()
                price_range = list(range(int(mini), int(maxi)))
                ser = []
                for product in products:
                    for n in price_range:
                        if product['product_price'] == n:
                            product = Products.objects.filter(product_id=product['product_id'])
                            print(product)
                            serializer = ProductsSerializer(product, many=True)
                            ser.append(serializer.data)
                return Response(ser, status=status.HTTP_200_OK)
            else:
                raise Exception
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductByUser(GenericAPIView):
    serializer_class = ProductsSerializer

    def get(self, request):
        try:
            seller_id = request.headers.get('Authorization')
            seller = Seller.objects.get(seller_id=seller_id)
            product = Products.objects.filter(instance=seller)
            serializer = self.serializer_class(product, many=True)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductStatus(GenericAPIView):
    def get(self, request):
        try:
            product_id = request.headers.get('Authorization')
            product = Products.objects.get(product_id=product_id)
            if product.product_status == 0:
                product.product_status = 1
            elif product.product_status == 1:
                product.product_status = 0
            else:
                raise Exception
            product.save()
            return Response({"success": True, "msg": "Status is Changed"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TicketAPI(GenericAPIView):
    def get(self, request):
        try:
            product_id = request.headers.get('Authorization')
            product = Products.objects.get(product_id=product_id)
            tickets = product.ticket_sold
            return Response({"success": True, "Ticket Sold": tickets}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductRatingFilter(GenericAPIView):

    def get(self, request):
        try:
            rating = request.GET.get('rating')
            print(rating)
            products = Products.objects.filter(product_rating__gte=rating)
            if products:
                ser = []
                for product in products:
                    serializer = ProductsSerializer(product)
                    ser.append(serializer.data)
                return Response(ser)
            else:
                raise Exception("Product Does Not Exist")
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderAPI(GenericAPIView):
    serializer_class = OrderSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response({"success": True, "msg": "Product is own its way"},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False, "msg": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            product_id = request.headers.get('Authorization')
            product = Products.objects.get(product_id=product_id)
            order = Order.objects.get(product=product)
            order.order_delivered = True
            order.save()
            return Response({"success": True, "msg": "Order Delivered"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"success": False, "msg": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
