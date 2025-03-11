from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .neo_models import UserNode  # Import the Neo4j UserNode model

@receiver(post_save, sender=User)
def create_user_node(sender, instance, created, **kwargs):
    """Create a UserNode in Neo4j when a new user is registered."""
    if created:  # Only create a node if it's a new user
        UserNode(username=instance.username).save()
