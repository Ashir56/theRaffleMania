from rest_framework import serializers
from .models import Products, ProductBuyer,\
    Wishlist, Reviews, Order


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'
        read_only_fields = ('genericmodels_ptr',)

    def validate(self, data):
        # if data['product_size']:
        #     data['product_size'] = [data.get('product_size')]
        image1 = data.get('product_image1')
        image2 = data.get('product_image2')
        image3 = data.get('product_image3')
        image4 = data.get('product_image4')
        image5 = data.get('product_image5')
        image6 = data.get('product_image6')
        image7 = data.get('product_image7')
        image8 = data.get('product_image8')
        image9 = data.get('product_image9')
        image10 = data.get('product_image10')

        images = [str(image1), str(image2), str(image3), str(image4), str(image5), str(image6), str(image7),
                  str(image8), str(image9), str(image10)]

        data['product_imageList'] = images

        return data


class ProductBuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBuyer
        fields = '__all__'
        read_only_fields = ('cartmodel_ptr',)


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'

    def validate(self, data):
        if data.get('buyer') is None:
            raise Exception('Buyer Field Can not be None')
        if data.get('product') is None:
            raise Exception('Product Field can not be none')
        product_id = data.get('product')
        products = Wishlist.objects.all()
        for product in products:
            if product_id.product_id == product.product_id:
                raise Exception('Product Already Exist')

        return data

    def create(self, validated_data):
        self.validate(validated_data)
        return super().create(validated_data)


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
