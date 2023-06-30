from django.db import models
from ContentPage.models import Products, ProductSize,Size


from django.conf import settings
from django.db.models.signals import post_save

class OrderItem(models.Model):

    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    size = models.ForeignKey(Size ,on_delete=models.CASCADE, related_name='sssize', default = None)

    def __str__(self) -> str:
        return self.product.model_name
    
    def get_orderItem_price(self) -> int:
        price = self.product.price * self.quantity
        return price
    
class Order(models.Model):

    ip =  models.CharField(max_length=15)
    items = models.ManyToManyField(OrderItem)
    ref_code = models.CharField(max_length=15)
    is_ordered = models.BooleanField(default=False)
    #date_ordered = models.DateTimeField()

    def get_cart_items(self):
        return self.items.all()
    
    @property
    def get_cart_total(self):
        
        return sum( [item.product.price * item.quantity for item in self.items.all()] )
    
    def __str__(self) -> str:
        return f'{self.id}, {self.ref_code}'