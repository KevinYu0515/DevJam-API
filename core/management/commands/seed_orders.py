from django.core.management.base import BaseCommand
from core.models import Order, Product, User
import random

class Command(BaseCommand):
    help = 'Seed the database with 5 orders'

    def handle(self, *args, **kwargs):
        products = list(Product.objects.all())
        users = list(User.objects.all())

        if not products or not users:
            self.stdout.write(self.style.ERROR('Please ensure Products and Users exist before seeding orders.'))
            return

        for i in range(5):
            product = random.choice(products)
            user = random.choice(users)
            amount = random.randint(1, 5)

            order = Order.objects.create(
                product=product,
                user=user,
                amount=amount,
            )
            self.stdout.write(self.style.SUCCESS(f'Created Order {order.id}: User {user.username} bought {amount} of {product.name}'))