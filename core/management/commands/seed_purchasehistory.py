from django.core.management.base import BaseCommand
from core.models import PurchaseHistory, ShopItem
import random

class Command(BaseCommand):
    help = 'Seed the database with 5 purchase history records'

    def handle(self, *args, **kwargs):
        shop_items = list(ShopItem.objects.all())
        if not shop_items:
            self.stdout.write(self.style.ERROR("請先建立 ShopItem 資料"))
            return

        for _ in range(5):
            item = random.choice(shop_items)
            PurchaseHistory.objects.create(
                itemID=item,
                amount=random.randint(1, 5)
            )
            self.stdout.write(self.style.SUCCESS(f"Created purchase record for: {item.itemName}"))
