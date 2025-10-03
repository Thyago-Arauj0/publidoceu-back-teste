from django.db import models
from api.card.models import Card  # referência ao Card

class FileCard(models.Model):
    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        verbose_name='Card',
        null=False,
        blank=False,
        related_name="files",
    )

    is_approved = models.BooleanField(
        verbose_name='Está aprovado',
        null=True,
        blank=True,
        default=False
    )

    file = models.URLField(
        verbose_name='Arquivo',
        default='https://upload.wikimedia.org/wikipedia/commons/a/a3/Image-not-found.png'
    )

    class Meta:
        verbose_name = 'Arquivo do Card'
        verbose_name_plural = 'Arquivos de Cards'

    def __str__(self):
        return f'Arquivo {self.id} ref. {self.card.title}'
