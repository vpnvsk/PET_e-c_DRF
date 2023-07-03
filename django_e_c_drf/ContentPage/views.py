from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import F 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets


from .models import Products, Size
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
        serializer = CreateOrderItemSerializer(data = request.data)
        print(serializer.initial_data)
        ip = get_client_ip(request)
        

        order, created = Order.objects.get_or_create(ip = ip, is_ordered = False)
        
        if serializer.is_valid():
            print(serializer.data['quantity'])
            print(serializer.data['quantity'] == 0)
            print(type(serializer.data['quantity']))


            if serializer.data['quantity'] == 0:
                
                ord = get_object_or_404(OrderItem,
                                        product = Products.objects.get(id = serializer.data['product']),
                                        size = Size.objects.get(id = serializer.data['size']),
                                        is_ordered = False,
                                        order = order,
                                        )               
            else:

                order_item, created = OrderItem.objects.get_or_create(
                    product = Products.objects.get(id = serializer.data['product']),
                    size = Size.objects.get(id = serializer.data['size']),
                    is_ordered = False,
                    order = order,
                )
                if created:
                    order_item.quantity = serializer.data['quantity']
                    order_item.save()
                else:
                    delete_var = order_item.quantity + serializer.data['quantity']
                    if delete_var == 0:
                        order_item.delete()
                    else:
                        order_item.quantity = F('quantity') + serializer.data['quantity']   
                        order_item.save()
                    
                    
            # product_ = serializer.save()

            
            # order = Order.objects.get_or_create(ip = ip, is_ordered = False)
            # product_.order.add(order.id)
            # order_qs = Order.objects.get_or_create(ip=ip, is_ordered = False)
            # order = order_qs[0]
            # print(order.items.all())
            

            # o = order.items.filter(product = product_.product,
            # size = product_.size,)
            # if o.exists():
            #     print('hello from if')
            #     ord = o[0]
            #     print(ord.quantity)
            #     print(ord)
            #     o.update(quantity=F('quantity')+product_.quantity) 
            #     if F('quantity') == 0:
            #         print('dddeleted')
            #         ord.delete()
            #         print('deleted')
                
                
            # else:
            #     print('hello from else')
                # order.items.add(product_.id)

                

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