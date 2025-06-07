from django.core.management.base import BaseCommand
from core.models import Product

class Command(BaseCommand):
    help = 'Seed the database with sample product data'

    def handle(self, *args, **kwargs):
        products = [
            {"name": "牙刷", "price": 35.0, "image": "https://example.com/images/toothbrush.jpg"},
            {"name": "牙膏", "price": 45.0, "image": "https://example.com/images/toothpaste.jpg"},
            {"name": "洗髮精", "price": 120.0, "image": "https://example.com/images/shampoo.jpg"},
            {"name": "沐浴乳", "price": 130.0, "image": "https://example.com/images/bodywash.jpg"},
            {"name": "洗衣精", "price": 180.0, "image": "https://example.com/images/laundry_detergent.jpg"},
            {"name": "垃圾袋", "price": 25.0, "image": "https://example.com/images/trash_bag.jpg"},
            {"name": "面紙", "price": 30.0, "image": "https://example.com/images/tissue.jpg"},
            {"name": "馬桶清潔劑", "price": 75.0, "image": "https://example.com/images/toilet_cleaner.jpg"},
            {"name": "洗碗精", "price": 50.0, "image": "https://example.com/images/dish_soap.jpg"},
            {"name": "拖把", "price": 250.0, "image": "https://example.com/images/mop.jpg"},
        ]
        Product.objects.bulk_create([Product(**data) for data in products])
        self.stdout.write(self.style.SUCCESS('Seeded 10 products successfully.'))