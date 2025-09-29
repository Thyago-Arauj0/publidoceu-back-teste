from django.db import models

from api.card.models import Card

class Checklist(models.Model):

    card = models.ForeignKey(
        Card, on_delete=models.CASCADE,
        verbose_name='Card',
        null=True, blank=True
    )

    title = models.CharField(
        verbose_name='Título',
        max_length=155,
        null=False,
        blank=True
    )

    is_check = models.BooleanField(

        verbose_name='Está feito',
        null=False, blank=False,
        default=False

    )

    created_at = models.DateTimeField(
        verbose_name='Criado em',
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        verbose_name='Atualizado em',
        auto_now=True
    )

    def __str__(self):
        # Verifica se card existe para não quebrar
        if self.card and self.card.board and self.card.board.customer:
            return f'Checklist de {self.card.board.customer.name}'
        return f'Checklist sem card'
