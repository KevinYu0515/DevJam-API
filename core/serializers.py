from rest_framework import serializers
from .models import Product, Order, ShopOwner, ShopItem, PurchaseHistory

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