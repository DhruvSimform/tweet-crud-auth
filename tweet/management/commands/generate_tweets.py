import random
from faker import Faker
from django.core.management.base import BaseCommand
from tweet.models import Tweet  # Adjust based on your app
from django.contrib.auth.models import User

fake = Faker()

class Command(BaseCommand):
    help = "Generate random tweets for random users"

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, nargs='?', default=100, help='Number of tweets to generate')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        users = list(User.objects.all())  # Get all users

        if len(users) < 1:
            self.stdout.write(self.style.ERROR("No users found. Create users first."))
            return

        tweets = [Tweet(user=random.choice(users), text=fake.sentence()) for _ in range(count)]
        Tweet.objects.bulk_create(tweets)

        self.stdout.write(self.style.SUCCESS(f"Successfully created {count} random tweets for random users!"))
