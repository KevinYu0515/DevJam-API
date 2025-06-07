from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView
)
from core.views import MyTokenObtainPairView

urlpatterns = [
    path('product/', views.product_list, name='product-list'),
    path('product/<int:pk>/', views.product_detail, name='product-detail'),
    path('order/', views.order_list, name='order-list'),
    path('order/<int:pk>/', views.order_detail, name='order-detail'),
    path('shopowner/', views.shopowner_list, name='shopowner-list'),
    path('shopowner/<int:pk>/', views.shopowner_detail, name='shopowner-detail'),
    path('shopitem/', views.shopitem_list, name='shopitem-list'),
    path('shopitem/<int:pk>/', views.shopitem_detail, name='shopitem-detail'),
    path('adduser/', views.adduser, name='adduser'),
    path('getuser/', views.getuser, name='getuser'),
    path('shopitem/<int:pk>/', views.shopitem_detail, name='shopitem-detail'),
    path('coin/', views.coin_list, name='coin-list'),
    path('coin/<int:pk>/', views.coin_detail, name='coin-detail'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),  # 登入
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 刷新
    path('purchase/', views.process_purchase, name='purchase')
]