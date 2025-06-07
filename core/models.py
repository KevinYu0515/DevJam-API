from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('normal', 'Normal User'),
        ('disadvantage', 'Disadvantaged User'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='normal')

# Create your models here.

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # 關聯到商品
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 關聯到使用者
    count = models.IntegerField(default=1)  # 購買數量
    ordertime = models.DateTimeField(auto_now_add=True)  # 訂單時間

    def __str__(self):
        return f"訂單 {self.id} - {self.product.name}"

class ShopOwner(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    headimage = models.ImageField(upload_to='shop_owners/', null=True, blank=True)

    def __str__(self):
        return self.name
