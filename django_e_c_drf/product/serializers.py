from rest_framework import serializers

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
        extra_kwargs = {'order':{'required': False},'product':{'required': False}}
        

    def create(self, validated_data):
        
        ip = self.context.get('ip')
        pk = self.context.get('pk')
        order = Order.objects.get(ip = ip, is_ordered = False)
        product = Products.objects.get(id = pk)
        validated_data.update({'order':order, 'product':product}) 
        order_item = OrderItem.objects.create(**validated_data)

        return order_item