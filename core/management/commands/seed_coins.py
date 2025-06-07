from django.core.management.base import BaseCommand
from core.models import Coin, User, ShopItem
import random
from django.utils import timezone

class Command(BaseCommand):
    help = 'Seed 300 Coin records'

    def handle(self, *args, **kwargs):
        users = list(User.objects.all())
        shop_items = list(ShopItem.objects.all())

        if len(users) < 1:
            self.stdout.write(self.style.ERROR("需要至少一位 User。"))
            return

        for i in range(100):
            sponsor = random.choice(users)
            owner = random.choice(users + [None])  # 有些可以沒有 owner
            item = random.choice(shop_items + [None])  # 有些可以沒有 item
            used_time = timezone.now() if item else None  # 若有使用就給時間

            Coin.objects.create(
                sponsor=sponsor,
                owner=owner,
                itemID=item,
                usedTime=used_time
            )

        self.stdout.write(self.style.SUCCESS("成功新增 300 筆 Coin 資料。"))
