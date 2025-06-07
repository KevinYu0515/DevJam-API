from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello_world),
    path('product/', views.product_list, name='product-list'),
    path('product/<int:pk>/', views.product_detail, name='product-detail'),
    path('order/', views.order_list, name='order-list'),
    path('order/<int:pk>/', views.order_detail, name='order-detail'),
    path('shopowner/', views.shopowner_list, name='shopowner-list'),
]