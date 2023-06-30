from rest_framework import serializers

from .models import Order, OrderItem
from .service import get_client_ip
from ContentPage.models import Products


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
        exclude = ['is_ordered', 'id']


class CartSerializer(serializers.ModelSerializer):
    
    final_value = serializers.CharField(source = 'get_cart_total', read_only = True)
    items = ItemOrderSerializer(many = True)
    class Meta:
        model = Order
        fields = ('items', 'final_value')
