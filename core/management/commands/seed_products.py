from django.core.management.base import BaseCommand
from core.models import Product

class Command(BaseCommand):
    help = 'Seed the database with sample product data'

    def handle(self, *args, **kwargs):
        products = [
            {"name": "牙刷", "price": 35.0, "image": "https://img.cloudimg.in/uploads/shops/40034/products/c5/c5288793202e32d5bf0a7ca5b603b30b.png"},
            {"name": "牙膏", "price": 45.0, "image": "https://www.whitemen-shopping.com.tw/storage/system/Product/toothpaste/WM030/030-2.jpg"},
            {"name": "洗髮精", "price": 120.0, "image": "https://cdn.cybassets.com/media/W1siZiIsIjg1OTYvcHJvZHVjdHMvZjc4OGFlYzc2MWJiNmU0NDA1YWZhMDlkM2EwZGE5MDgzN2M4MGYxMmJiNDIyODM0NDk2YzEwNmZhMzQwZGY1NS5qcGVnIl0sWyJwIiwidGh1bWIiLCI2MDB4NjAwIl1d.jpeg?sha=673ce5c84709eb33"},
            {"name": "沐浴乳", "price": 130.0, "image": "https://diz36nn4q02zr.cloudfront.net/webapi/imagesV3/Original/SalePage/9947357/0/638847388091170000?v=1"},
            {"name": "洗衣精", "price": 180.0, "image": "https://cdn.cybassets.com/media/W1siZiIsIjg1OTYvcHJvZHVjdHMvZTExZDBlOTM4NDc5Mjg0OTgwM2E1OWQxMTFiNTViMTc3MTVjYjM4ZTIxMDY0ZmI3MzZkZWZkYzdjZjc4NzdmYS5qcGVnIl0sWyJwIiwidGh1bWIiLCIxMDI0eDEwMjQiXV0.jpeg?sha=906785acd880fd30"},
            {"name": "垃圾袋", "price": 25.0, "image": "https://static.iyp.tw/40735/products/photooriginal-2012576-HLNyE.jpg"},
            {"name": "面紙", "price": 30.0, "image": "https://eatfoodgod.com/wp-content/uploads/2022/04/product_20220311161008461_b.jpg"},
            {"name": "馬桶清潔劑", "price": 75.0, "image": "https://i4.momoshop.com.tw/1692548286/goodsimg/0004/128/774/4128774_O_m.webp"},
            {"name": "洗碗精", "price": 50.0, "image": "https://rs.joo.com.tw/website/uploads_product/website_923/P0092300101979_1_856522.png?_19883"},
            {"name": "拖把", "price": 250.0, "image": "https://www.kfcshop.com.tw/images/202310/cl40367.jpg"},
        ]

        names = [u['name'] for u in products]
        deleted_count, _ = Product.objects.filter(name__in=names).delete()
        self.stdout.write(self.style.WARNING(f"Deleted {deleted_count} existing products."))

        Product.objects.bulk_create([Product(**data) for data in products])
        self.stdout.write(self.style.SUCCESS('Seeded 10 products successfully.'))