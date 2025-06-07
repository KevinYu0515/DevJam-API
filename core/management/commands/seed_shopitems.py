from django.core.management.base import BaseCommand
from core.models import ShopItem, ShopOwner
import random

class Command(BaseCommand):
    help = 'Seed the database with 5 shop items'

    def handle(self, *args, **kwargs):
        shop_owners = list(ShopOwner.objects.all())
        if not shop_owners:
            self.stdout.write(self.style.ERROR("請先建立 ShopOwner"))
            return

        items = [
            {"itemName": "原子筆", "price": 15},
            {"itemName": "筆記本", "price": 40},
            {"itemName": "便利貼", "price": 25},
            {"itemName": "訂書機", "price": 80},
            {"itemName": "剪刀", "price": 35},
        ]

        for item in items:
            shop = random.choice(shop_owners)
            ShopItem.objects.create(
                shopID=shop,
                itemName=item["itemName"],
                price=item["price"]
            )
            self.stdout.write(self.style.SUCCESS(f"Created ShopItem: {item['itemName']} at {shop.name}"))
