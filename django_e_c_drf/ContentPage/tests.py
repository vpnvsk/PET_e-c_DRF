from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Products, Brand, Size, ProductSize, Image


class ContentPageTest(APITestCase):


    def setUp(self):
        brand = Brand.objects.create(name = 'test_name')
        size = Size.objects.create(size_name = '1')
        image = Image.objects.create(name='test_image')
        self.product = Products.objects.create(brand = brand, model_name = 'test_model_name',price = 1,images = image)
        self.product.sizes.add(size,)
        ProductSize.objects.create(size = size, product=self.product, count=1)

        self.data = {
            "size":size,
            "quantity": 1

        }

    def test_product_list(self):
        response = self.client.get(reverse('list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


    def test_product(self):
        response = self.client.get(reverse('product', kwargs={'pk':self.product.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('brand'), 'test_name')


    # def test_fail_product(self):
    #     response = self.client.get(reverse('product', kwargs={'pk':2}))
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) 

    
    def test_create_order(self):
        response = self.client.post(reverse('product', kwargs={'pk':self.product.id}), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
