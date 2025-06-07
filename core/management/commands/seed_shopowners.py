from django.core.management.base import BaseCommand
from core.models import ShopOwner

class Command(BaseCommand):
    help = 'Seed the database with 2 shop owners'

    def handle(self, *args, **kwargs):
        owners = [
            {"name": "小王便利店", "location": "台北市中正區", "headimage": "https://example.com/images/shop1.jpg"},
            {"name": "阿美超市", "location": "新北市板橋區", "headimage": "https://example.com/images/shop2.jpg"},
        ]

        for odata in owners:
            obj, created = ShopOwner.objects.get_or_create(
                name=odata["name"],
                defaults={
                    "location": odata["location"],
                    "headimage": odata["headimage"],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created ShopOwner: {obj.name}"))
            else:
                self.stdout.write(f"ShopOwner {obj.name} already exists.")