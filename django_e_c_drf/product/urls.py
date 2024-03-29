from django.urls import path

from . import views

urlpatterns = [
    path('products/', views.ProductViewSet.as_view({'get':'list'}), name = 'list'),
    path('products/<int:pk>', views.ProductDetailedView.as_view(), name = 'product'),
]