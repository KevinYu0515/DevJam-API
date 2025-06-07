from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('normal', 'Normal User'),
        ('disadvantage', 'Disadvantaged User'),
        ('admin', 'Admin'),
    )
    created_time = models.DateTimeField(auto_now_add=True)
    headImage = models.URLField(blank=True, null=True)
    account = models.CharField(max_length=100, blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='normal')

    def get_user_type(self):
        if hasattr(self, 'normaluser'):
            return 'normal'
        if hasattr(self, 'disadvantageuser'):
            return 'disadvantage'
        if hasattr(self, 'adminuser'):
            return 'admin'
        return 'unknown'

class NormalUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='normaluser')
    # 可擴充 NormalUser 特有欄位

class DisadvantageUser(models.Model):
    LEVEL_CHOICES = (
        ('level 1', 'Level 1'),
        ('level 2', 'Level 2'),
        ('level 3', 'Level 3'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='disadvantageuser')
    category = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='level 1')

class AdminUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='adminuser')
    # 可擴充 AdminUser 特有欄位

# Create your models here.

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.TextField()
    amount = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # 關聯到商品
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 關聯到使用者
    amount = models.IntegerField(default=1)  # 購買數量
    ordertime = models.DateTimeField(auto_now_add=True)  # 訂單時間

    def __str__(self):
        return f"訂單 {self.id} - {self.product.name}"

class ShopOwner(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    headimage = models.TextField()

    def __str__(self):
        return self.name

class ShopItem(models.Model):
    id = models.AutoField(primary_key=True)
    shopID = models.ForeignKey(ShopOwner, on_delete=models.CASCADE)  # 關聯到商店
    itemName = models.CharField(max_length=200)
    price = models.IntegerField()

    def __str__(self):
        return f"{self.itemName} - {self.shop.name}"

class PurchaseHistory(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)   # Temporary string field for user ID
    itemID = models.ForeignKey(ShopItem, on_delete=models.CASCADE)  # Reference to ShopItem
    purchase_time = models.DateTimeField(auto_now_add=True)  # Purchase timestamp
    amount = models.IntegerField(default=0)  # 設定預設值為1

    def __str__(self):
        return f"Purchase {self.id} - {self.itemID.itemName}"

class Coin(models.Model):
    id = models.AutoField(primary_key=True)
    createTime = models.DateTimeField(auto_now_add=True)
    sponsor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sponsored_coins')
    #sponsor = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='owned_coins')
    usedTime = models.DateTimeField(null=True, blank=True)
    itemID = models.ForeignKey(ShopItem, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Coin {self.id} - Sponsored by {self.sponsor.username}"
