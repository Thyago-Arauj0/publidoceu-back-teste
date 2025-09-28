from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet

from .models import Checklist
from .serializers import ChecklistSerializer

from rest_framework.permissions import (

    IsAdminUser

)

from api.board.models import Board

class ChecklistViewSet(ModelViewSet):

    permission_classes = [IsAdminUser]
    serializer_class = ChecklistSerializer

    def get_queryset(self):

        board_id = self.kwargs.get('board_pk')
        user = self.request.user

        if board_id is None:

            return Checklist.objects.none()

        if user.is_staff or user.is_superuser:

            return Checklist.objects.filter(board_id=board_id).order_by('-id')

        return Checklist.objects.none()

    def perform_create(self, serializer):
        
        board_id = self.kwargs.get('board_pk')
        board = get_object_or_404(Board, pk=board_id)

        serializer.save(board=board)
