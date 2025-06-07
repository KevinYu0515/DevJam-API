from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import NormalUser, DisadvantageUser, AdminUser

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

        # 先刪除所有這些 username 的使用者（含子模型依照你DB設定）
        usernames = [u['username'] for u in users_data]
        deleted_count, _ = User.objects.filter(username__in=usernames).delete()
        self.stdout.write(self.style.WARNING(f"Deleted {deleted_count} existing users."))

        created_count = 0
        for udata in users_data:
            if User.objects.filter(username=udata["username"]).exists():
                self.stdout.write(f"User {udata['username']} already exists.")
                continue

            user = User.objects.create_user(
                username=udata["username"],
                email=udata["email"],
                password=udata["password"],
                user_type=udata["user_type"],
            )

            # 根據 user_type 建立子表
            if udata["user_type"] == "normal":
                NormalUser.objects.create(user=user)
            elif udata["user_type"] == "disadvantage":
                category = udata.get("category", "level 1")
                DisadvantageUser.objects.create(user=user, category=category)
            elif udata["user_type"] == "admin":
                AdminUser.objects.create(user=user)

            created_count += 1
            self.stdout.write(self.style.SUCCESS(f"Created user {user.username} with type {user.user_type}"))

            self.stdout.write(self.style.SUCCESS(f'Seeded {created_count} users successfully.'))
