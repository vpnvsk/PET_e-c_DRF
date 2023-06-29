from django.contrib import admin
from .models import Products, Brand, Image, ProductSize, Size


@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('brand','model_name')

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')

 
@admin.register(ProductSize)
class ProductSizeInline(admin.ModelAdmin):
    list_display = ('size', 'product')

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('size_name', 'id')
