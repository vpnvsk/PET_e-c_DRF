from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import F 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets


from .models import Products
from .serializers import ProductListSerializers, ProductDetailedSerializer, CreateOrderItemSerializer
from cart.service import get_client_ip
from cart.models import Order, OrderItem


class ProductListView(APIView):

    def get(self, request):
        products = Products.objects.all()
        serializer = ProductListSerializers(products, many = True)
        return Response(serializer.data)
    

class ProductDetailedView(APIView):

    def get(self,request, pk):
        product = Products.objects.get(id=pk)
        serializer = ProductDetailedSerializer(product)
        return Response(serializer.data)
    
    def post(self, request, pk):
        serializer = CreateOrderItemSerializer( data=request.data)
        print(serializer.initial_data)
        if serializer.is_valid():
            product_ = serializer.save()
            ip = get_client_ip(request)
            

            order_qs = Order.objects.get_or_create(ip=ip)
            order = order_qs[0]
            print(order.items.all())
            

            o = order.items.filter(product = product_.product,
            size = product_.size,)
            if o.exists():
                print('hello from if')
                ord = o[0]
                print(ord.quantity)
                o.update(quantity=F('quantity')+product_.quantity) 
                
                
            else:
                print('hello from else')
                order.items.add(product_.id)

                

            return Response(status=201)
        else:
            print(serializer.errors)
            return Response(status=400)
    
class ProductViewSet(viewsets.ViewSet):
    
    
    def list(self, request):
        queryset = Products.objects.all()
        serializer = ProductListSerializers(queryset, many = True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk):
        queryset = Products.objects.all()
        product = get_object_or_404(queryset)
        serializer = ProductDetailedSerializer(product)
        return Response(serializer.data)