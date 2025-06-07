from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed the database with sample users'

    def handle(self, *args, **kwargs):
        users_data = [
            {"username": "normaluser1", "password": "TestPass123", "email": "normal1@example.com", "user_type": "normal"},
            {"username": "normaluser2", "password": "TestPass123", "email": "normal2@example.com", "user_type": "normal"},
            {"username": "normaluser3", "password": "TestPass123", "email": "normal3@example.com", "user_type": "normal"},

            {"username": "disadvuser1", "password": "TestPass123", "email": "disadv1@example.com", "user_type": "disadvantage"},
            {"username": "disadvuser2", "password": "TestPass123", "email": "disadv2@example.com", "user_type": "disadvantage"},
            {"username": "disadvuser3", "password": "TestPass123", "email": "disadv3@example.com", "user_type": "disadvantage"},

            {"username": "adminuser", "password": "AdminPass123", "email": "admin@example.com", "user_type": "admin"},
        ]

        created_count = 0
        for udata in users_data:
            if not User.objects.filter(username=udata["username"]).exists():
                user = User.objects.create_user(
                    username=udata["username"],
                    email=udata["email"],
                    password=udata["password"],
                    user_type=udata["user_type"]
                )
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Created user {user.username} with type {user.user_type}"))
            else:
                self.stdout.write(f"User {udata['username']} already exists.")

        self.stdout.write(self.style.SUCCESS(f'Seeded {created_count} users successfully.'))
