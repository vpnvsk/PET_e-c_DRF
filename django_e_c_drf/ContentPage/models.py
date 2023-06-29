from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Brand(models.Model):

    name = models.CharField(max_length = 15)

    def __str__(self):
        return f'{self.name}'
    
    
class Image(models.Model):
        
    name = models.CharField(max_length=10)
    img1 = models.ImageField(upload_to='image/%Y')
    img2 = models.ImageField(upload_to='image/%Y')
    img3 = models.ImageField(upload_to='image/%Y')

    def __str__(self):
        return f'{self.name}'
    

class Size(models.Model):
    size_name = models.CharField(max_length=5)

    def __str__(self):
        return f'{self.size_name}'
    
    
class Products(models.Model):

    brand = models.ForeignKey(Brand, related_name='items', on_delete=models.CASCADE)
    model_name = models.CharField(max_length=20)
    price =  models.DecimalField(max_digits = 6, decimal_places = 2)
    images = models.ForeignKey(Image, on_delete=models.CASCADE)
    sizes = models.ManyToManyField(Size, through='ProductSize')
    

    def __str__(self):
        return f'{self.brand} {self.model_name}'
    
    def get_absolute_url(self):
        return reverse('productsContent:certain_product', kwargs={
            'slug': self.slug}
                
            )
            
    def get_add_to_cart_url(self):
        return reverse("cart:add-to-cart",kwargs={
            'pk': self.id
            })
    def get_delete_from_cart_url(self):
        return reverse("cart:remove-from-cart",kwargs={
            'pk': self.id
            })

class ProductSize(models.Model):
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)

    def get_count(self) -> int:
        return self.count   

