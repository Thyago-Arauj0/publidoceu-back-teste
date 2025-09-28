from django.db import models

from api.board.models import Board

class Checklist(models.Model):

    board = models.ForeignKey(
        Board, on_delete=models.CASCADE,
        verbose_name='Cliente',
        null=False, blank=False
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

        return f'Checklist de {self.board.customer.name}'