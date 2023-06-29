from rest_framework import serializers
from django.shortcuts import get_object_or_404

from .models import Products, Brand, ProductSize
from cart.models import Order, OrderItem


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class ProductSizeSerializer(serializers.HyperlinkedModelSerializer):

    size = serializers.ReadOnlyField(source='size.size_name')
    class Meta:
        model = ProductSize
        fields = ('size', 'count',)
 

class ProductListSerializers(serializers.ModelSerializer):

    brand = serializers.SlugRelatedField(slug_field='name', read_only = True)
    class Meta:
        model = Products
        exclude = ['sizes']

class ProductDetailedSerializer(serializers.ModelSerializer):

    brand = serializers.SlugRelatedField(slug_field='name', read_only = True)
    sizes = ProductSizeSerializer(source='productsize_set', many=True)
    class Meta:
        model = Products
        fields = '__all__'

class CreateOrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        exclude = ('is_ordered',)

    def create(self, validated_data):
    
        order, created = OrderItem.objects.update_or_create(
            product = validated_data.get('product',None),
            quantity = validated_data.get('quantity', None),
            size = validated_data.get('size',None),
        )
        return order