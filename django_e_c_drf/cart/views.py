from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import F 


from .service import get_client_ip
from .serializers import CartSerializer, UpdateCartSerializer, DeleteFromCartSerializer
from .models import Order, OrderItem
from product.models import Products, Size


class CartView(APIView):

    def get(self, request):

        ip = get_client_ip(request)
        
        client = Order.objects.get(ip=ip, is_ordered=False)

        serializer = CartSerializer(client)

        return Response(serializer.data)
    
    def put(self, request):
        serializer = UpdateCartSerializer(data=request.data)
        if serializer.is_valid():
            ip = get_client_ip(request)

            order = get_object_or_404(Order, ip=ip)
            product_id = serializer.validated_data['product_id']
            item = OrderItem.objects.filter(
                                                order=order,
                                                id=product_id
                                            )
            if item.exists():
                
                item.update(quantity = F('quantity') + serializer.validated_data['quantity'])

                return Response(status=201)
        
        return Response(status=400)
    def delete(self, request):
        serializer = DeleteFromCartSerializer(data=request.data)
        if serializer.is_valid():
            ip = get_client_ip(request)

            product_id = serializer.validated_data['product_id']

            order = Order.objects.filter(
                ip=ip, is_ordered=False,
            ).first()

            if order:
                
                order_item = OrderItem.objects.filter(
                                                order=order,
                                                id=product_id
                                            )

                if order_item:
                    order_item.delete()
                    return Response({"message": "Item deleted from cart successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Item not found in the cart"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"error": "No active order found for the given IP address"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    