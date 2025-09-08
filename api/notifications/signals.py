from django.db.models.signals import post_save
from django.dispatch import receiver

from api.card.models import Card, Feedback

from .models import Notification

@receiver(post_save, sender=Card)
def notify_card_user(sender, instance, created, **kwargs):

    if created:
        
        Notification.objects.create(
            user=instance.admin,
            message=f"Novo pedido criado pelo cliente {instance.customer}"
        )

@receiver(post_save, sender=Feedback)
def notify_feedback_admin(sender, instance, created, **kwargs):

    if created:

        Notification.objects.create(
            user=instance.admin,
            message=f"Novo pedido criado pelo cliente {instance.customer}"
        )
