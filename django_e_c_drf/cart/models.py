from django.db import models
from ContentPage.models import Products, ProductSize,Size


from django.conf import settings
from django.db.models.signals import post_save


    
class Order(models.Model):

    ip =  models.CharField(max_length=15)
    ref_code = models.CharField(max_length=15)
    is_ordered = models.BooleanField(default=False)
    #date_ordered = models.DateTimeField()

    # def get_cart_items(self):
    #     return self.item.all()
    
    @property
    def get_cart_total(self) -> int:
        
        return sum( [item.product.price * item.quantity for item in self.item.all()] )
    
    def __str__(self) -> str:
        return f'{self.id}, {self.ref_code}'


class OrderItem(models.Model):

    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    size = models.ForeignKey(Size ,on_delete=models.CASCADE, related_name='sssize', default = None)
    order = models.ForeignKey(Order, related_name="item", on_delete=models.CASCADE, default= None)

    def __str__(self) -> str:
        return self.product.model_name
    
    def get_orderItem_price(self) -> int:
        price = self.product.price * self.quantity
        return price