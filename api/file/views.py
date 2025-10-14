from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from api.supabase_utils import delete_from_supabase
from api.cloudinary_utils import delete_from_cloudinary
from .models import FileCard
from .serializers import FileCardSerializer
from api.card.models import Card

class FileCardViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = FileCardSerializer

    def perform_destroy(self, instance):

        if instance.file:

            # delete_from_supabase(instance.file)
            delete_from_cloudinary(instance.file)
            
        instance.delete()

    def get_queryset(self):

        card_id = self.kwargs.get('card_pk')

        if card_id is None:

            return FileCard.objects.none()
        
        return FileCard.objects.filter(card_id=card_id).order_by('-id')

    def perform_create(self, serializer):

        card_id = self.kwargs.get('card_pk')

        card_instance = get_object_or_404(Card, pk=card_id)

        serializer.save(card=card_instance)
