from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

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
    category = serializers.SerializerMethodField()
    # 定義使用者模型對應的序列化器
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type', 'created_time', 'headImage', 'account', 'category']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def get_category(self, obj):
        if obj.user_type == 'disadvantage' and hasattr(obj, 'disadvantageuser'):
            return obj.disadvantageuser.category
        return None

    def create(self, validated_data):
        user_type = validated_data.get('user_type', 'normal')
        password = validated_data.pop('password')
        
        # 先創建 User 實例
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # 根據 user_type 創建對應子模型
        if user_type == 'normal':
            NormalUser.objects.create(user=user)
        elif user_type == 'disadvantage':
            # DisadvantageUser 需要 category 預設 level 1
            DisadvantageUser.objects.create(user=user, category='level 1')
        elif user_type == 'admin':
            AdminUser.objects.create(user=user)

        return user

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

class LoginSerializer(serializers.Serializer):
    account = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        account = data.get('account')
        password = data.get('password')
        try:
            user = User.objects.get(account=account)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid account or password')
        if not user.check_password(password):
            raise serializers.ValidationError('Invalid account or password')

        refresh = RefreshToken.for_user(user)

        # 自訂加入欄位到 access token payload
        refresh['uid'] = user.id
        refresh['username'] = user.username
        refresh['user_type'] = user.user_type
        refresh['account'] = user.account
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }