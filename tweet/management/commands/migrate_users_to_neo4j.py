from django.core.management.base import BaseCommand
from tweet.models import User  # Import Django user model
from tweet.neo_models import UserNode  # Import Neo4j user node

class Command(BaseCommand):
    help = "Migrate existing users from SQLite to Neo4j"

    def handle(self, *args, **kwargs):
        existing_users = User.objects.all()
        count = 0

        for user in existing_users:
            # Ensure we don't create duplicate nodes
            if not UserNode.nodes.filter(username=user.username):
                UserNode(username=user.username).save()
                count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully migrated {count} users to Neo4j!'))
