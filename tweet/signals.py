from django.db.models.signals import post_save,pre_save , post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .neo_models import UserNode  # Import the Neo4j UserNode model
from .models import Profile

@receiver(post_save, sender=User)
def create_user_node(sender, instance, created, **kwargs):
    """Create a UserNode in Neo4j when a new user is registered."""
    if created:  # Only create a node if it's a new user
        UserNode(username=instance.username).save()
        # Create a corresponding Profile instance
        Profile.objects.create(user=instance.user)

@receiver(pre_save, sender=User)
def update_user_node(sender, instance, **kwargs):
    """Update the Neo4j UserNode when the username changes."""
    if instance.pk:  # Ensure it's an existing user
        try:
            old_user = User.objects.get(pk=instance.pk)
            if old_user.username != instance.username:  # Check if username has changed
                user_node = UserNode.nodes.get(username=old_user.username)
                user_node.username = instance.username
                user_node.save()
        except (User.DoesNotExist, UserNode.DoesNotExist):
            pass  # If user/node does not exist, do nothing

@receiver(post_delete, sender=User)
def delete_user_node(sender, instance, **kwargs):
    """Delete the Neo4j UserNode and all its relationships when a user is deleted."""
    try:
        user_node = UserNode.nodes.get(username=instance.username)
        user_node.delete()  # Deletes the node along with all its connections
    except UserNode.DoesNotExist:
        pass  # If node does not exist, do nothing