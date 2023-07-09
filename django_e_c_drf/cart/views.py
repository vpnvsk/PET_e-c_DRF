from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import F 


from .service import get_client_ip
from .serializers import CartSerializer, DeleteFromCartSerializer
from .models import Order, OrderItem
from ContentPage.models import Products, Size


class CartView(APIView):

    def get(self, request):

        ip = get_client_ip(request)
        client = Order.objects.get(ip = ip, is_ordered = False)

        serializer = CartSerializer(client)

        return Response(serializer.data)
    
    def post(self, request):
        serializer = DeleteFromCartSerializer(data=request.data)
        if serializer.is_valid():
            ip = get_client_ip(request)
            item = OrderItem.objects.filter(order = Order.objects.get(ip=ip),
                                            product = Products.objects.get(model_name = serializer.validated_data['product']),
                                            size = Size.objects.get(size_name = serializer.validated_data['size'])
                                            )
            match serializer.validated_data['status']:

                case 'INC':                
                    item.update(quantity = F('quantity') + 1)
                case 'DEC':
                    item.update(quantity = F('quantity') - 1)
                case 'DEL':
                    item.delete()
            return Response(status=201)
        else:
            return Response(status=400)
