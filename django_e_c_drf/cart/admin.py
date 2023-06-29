from django.contrib import admin
from .models import Order, OrderItem

@admin.register(Order)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','ref_code')

@admin.register(OrderItem)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','product')