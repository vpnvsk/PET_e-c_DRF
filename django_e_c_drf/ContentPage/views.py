from django.shortcuts import get_object_or_404
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
    
    def post(self, request, pk, format = None):

        ip = get_client_ip(request)
        serializer = CreateOrderItemSerializer(data = request.data, context = {'ip':ip})
        print(serializer.initial_data)
        

        order, created = Order.objects.get_or_create(ip = ip, is_ordered = False)
        
        if serializer.is_valid():



            if serializer.validated_data['quantity'] == 0:
                
                ord = get_object_or_404(OrderItem,
                                        product = serializer.validated_data['product'],
                                        size =  serializer.validated_data['size'],
                                        is_ordered = False,
                                        order = order,
                                        )   
                ord.delete()            
            else:

                order_item, oi_created = OrderItem.objects.get_or_create(
                    product = serializer.validated_data['product'],
                    size = serializer.validated_data['size'],
                    is_ordered = False,
                    order = order,
                )
                if oi_created:
                    serializer.save()

                else:
                    delete_var = order_item.quantity + serializer.validated_data['quantity']
                    if delete_var == 0:
                        order_item.delete()
                    else:
                        order_item.quantity = F('quantity') + serializer.validated_data['quantity']   
                        order_item.save()

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