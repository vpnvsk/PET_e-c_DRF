from rest_framework import serializers

from .models import Order, OrderItem
from .service import get_client_ip
from product.models import Products, Size


class ProductOrderSerializer(serializers.ModelSerializer):

    brand = serializers.SlugRelatedField(slug_field='name', read_only = True)
    class Meta:
        model = Products
        fields = ('brand','model_name','price')


class ItemOrderSerializer(serializers.ModelSerializer):

    size = serializers.SlugRelatedField(slug_field='size_name',read_only = True)
    product = ProductOrderSerializer()
    class Meta:
        model = OrderItem
        exclude = ['is_ordered', 'order']


class CartSerializer(serializers.ModelSerializer):
    
    final_value = serializers.CharField(source = 'get_cart_total', read_only = True)
    item = ItemOrderSerializer(many = True)
    class Meta:
        model = Order
        fields = ('item', 'final_value')


class UpdateCartSerializer(serializers.Serializer):

    quantity = serializers.IntegerField()
    product_id = serializers.IntegerField()

class DeleteFromCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()





