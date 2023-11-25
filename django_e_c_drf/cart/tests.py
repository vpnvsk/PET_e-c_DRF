from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Order, OrderItem
from .serializers import CartSerializer
from product.models import Products, Brand, Size, ProductSize, Image



class CartTest(APITestCase):


    def setUp(self):
        brand = Brand.objects.create(name = 'test_name')
        size = Size.objects.create(size_name = '1')
        image = Image.objects.create(name='test_image')
        self.product = Products.objects.create(brand = brand, model_name = 'test_model_name',price = 1,images = image)
        self.product.sizes.add(size,)
        ProductSize.objects.create(size = size, product=self.product, count=1)

        self.add_to_cart = {
            "size":size.id,
            "quantity": 5
        }

        self.inc = {
            "product": 'test_model_name',
            "size":'1',
            "status":"INC"
        }

        self.dec = {
            "product": 'test_model_name',
            "size":'1',
            "status":"DEC"
        }

        self.delete = {
            "product": "test_model_name",
            "size":"1",
            "status":"DEL"
        }
    



    def test_cart(self):
        response = self.client.post(reverse('product', kwargs={'pk':self.product.id}), self.add_to_cart)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_get = self.client.get(reverse('cart'))
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(response_get.data['item'][0]['quantity'],5)


    def test_cart_inc(self):

        response = self.client.post(reverse('product', kwargs={'pk':self.product.id}), self.add_to_cart)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_post = self.client.post(reverse('cart'), self.inc)
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        response_get = self.client.get(reverse('cart'))
        self.assertEqual(response_get.data['item'][0]['quantity'],6)


    def test_cart_dec(self):

        response = self.client.post(reverse('product', kwargs={'pk':self.product.id}), self.add_to_cart)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_post = self.client.post(reverse('cart'), self.dec)
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        response_get = self.client.get(reverse('cart'))
        self.assertEqual(response_get.data['item'][0]['quantity'],4)


    def test_cart_del(self):

        response = self.client.post(reverse('product', kwargs={'pk':self.product.id}), self.add_to_cart)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_post = self.client.post(reverse('cart'), self.delete)
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        response_get = self.client.get(reverse('cart'))
        self.assertEqual(int(response_get.data['final_value']), 0)