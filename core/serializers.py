from rest_framework import serializers
from .models import Product, Order, ShopOwner, ShopItem, PurchaseHistory
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
    
from django.contrib.auth import get_user_model

# 商品序列化器：用於將 Product 模型轉換成 JSON 格式，以及將 JSON 資料轉換成 Product 模型
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        # 指定要序列化的模型
        model = Product
        # 指定要序列化的欄位
        fields = ['id', 'name', 'price', 'image']

class OrderSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)  # 顯示商品名稱

    class Meta:
        model = Order
        fields = ['id', 'product', 'product_name', 'user', 'amount', 'ordertime']
        read_only_fields = ['ordertime']  # 訂單時間自動生成，不可修改

class ShopOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopOwner
        fields = ['id', 'name', 'location', 'headimage']

class ShopItemSerializer(serializers.ModelSerializer):
    shop_name = serializers.CharField(source='shop.name', read_only=True)  # 顯示商店名稱

    class Meta:
        model = ShopItem
        fields = ['id', 'shopID', 'shop_name', 'itemName', 'price']

class PurchaseHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseHistory
        fields = ['id', 'itemID', 'purchase_time', 'amount'] 

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    # 定義使用者模型對應的序列化器
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'user_type', 'created_time', 'headImage', 'account']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # 使用 create_user 來正確處理密碼雜湊
        return User.objects.create_user(**validated_data)

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    # 定義使用者模型對應的序列化器
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'user_type', 'created_time', 'headImage', 'account']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # 使用 create_user 來正確處理密碼雜湊
        return User.objects.create_user(**validated_data)
from rest_framework import serializers
from .models import Product, Order, ShopOwner, ShopItem, PurchaseHistory, Coin

# 商品序列化器：用於將 Product 模型轉換成 JSON 格式，以及將 JSON 資料轉換成 Product 模型
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        # 指定要序列化的模型
        model = Product
        # 指定要序列化的欄位
        fields = ['id', 'name', 'price', 'image', 'amount']

class OrderSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)  # 顯示商品名稱

    class Meta:
        model = Order
        fields = ['id', 'product', 'product_name', 'user', 'count', 'ordertime']
        read_only_fields = ['ordertime']  # 訂單時間自動生成，不可修改

class ShopOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopOwner
        fields = ['id', 'name', 'location', 'headimage']

class ShopItemSerializer(serializers.ModelSerializer):
    shop_name = serializers.CharField(source='shop.name', read_only=True)  # 顯示商店名稱

    class Meta:
        model = ShopItem
        fields = ['id', 'shopID', 'shop_name', 'itemName', 'price']

class PurchaseHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseHistory
        fields = ['id', 'itemID', 'purchase_time', 'amount']

class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = ['id', 'createTime', 'sponsor', 'owner', 'usedTime', 'itemID']
        read_only_fields = ['id', 'createTime']  # 這些欄位只能讀取，不能修改 

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # 加入自訂欄位到 access token payload
        token['uid'] = user.id
        token['username'] = user.username
        token['user_type'] = user.user_type

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # 同時把這些資訊放在 response body，方便前端拿到

        return data