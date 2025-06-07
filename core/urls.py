from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView
)

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
    path('getuser/disadv/', views.getuser_disadv, name='getuser_disadv'),
    path('getuser/normal/', views.getuser_normal, name='getuser_normal'),
    path('shopitem/<int:pk>/', views.shopitem_detail, name='shopitem-detail'),
    path('coin/', views.coin_list, name='coin-list'),
    path('create_coin/', views.create_coin, name='create_coin'),
    path('login/', views.login, name='token_obtain_pair'),  # 登入
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 刷新
    path('api/purchase/', views.process_purchase, name='purchase'),
    path('parse_jwt/', views.parse_jwt, name='parse_jwt'),
    path('get_user_coins/<int:uid>/', views.get_user_coins, name='get_user_coins'),
    path('get_user_purchase_history/', views.get_user_purchase_history, name='get_user_purchase_history'),
]