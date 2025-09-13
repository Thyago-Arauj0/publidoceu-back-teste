from django.dispatch import receiver
from django.db.models.signals import post_save

from django.contrib.auth import get_user_model
from .models import Board

User = get_user_model()

@receiver(post_save, sender=User)
def create_board_user(sender, instance, created, **kwargs):
    
    if created:

        if not instance.is_staff and not instance.is_superuser:
            
            Board.objects.get_or_create(customer=instance, author=instance.author)
		