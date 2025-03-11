import random
from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

fake = Faker()

class Command(BaseCommand):
    help = "Generate 15 developer users with a default password"

    def handle(self, *args, **kwargs):
        users = []
        for i in range(15):
            username = f"dev{i+1}"
            email = fake.email()
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password="Root@123"
                )
                users.append(user)
        
        self.stdout.write(self.style.SUCCESS(f"Successfully created {len(users)} developer users with password Root@123"))
