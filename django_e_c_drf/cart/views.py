from rest_framework.response import Response
from rest_framework.views import APIView

from .service import get_client_ip
from .serializers import CartSerializer
from .models import Order


class CartView(APIView):

    def get(self, request):

        ip = get_client_ip(request)
        client = Order.objects.get(ip = ip, is_ordered = False)

        serializer = CartSerializer(client)

        return Response(serializer.data)

