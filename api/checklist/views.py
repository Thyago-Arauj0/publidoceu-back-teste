from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet

from .models import Checklist
from .serializers import ChecklistSerializer

from rest_framework.permissions import IsAuthenticated

from api.card.models import Card

class ChecklistViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = ChecklistSerializer

    def get_queryset(self):
        card_id = self.kwargs.get('card_pk')
        if card_id is None:
            return Checklist.objects.none()
        return Checklist.objects.filter(card_id=card_id).order_by('-id')



    def perform_create(self, serializer):
        card_id = self.kwargs.get('card_pk')  # ⚠️ tem que ser exatamente esse nome
        card_instance = get_object_or_404(Card, pk=card_id)
        serializer.save(card=card_instance)


