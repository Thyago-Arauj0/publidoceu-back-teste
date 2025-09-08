from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        user = request.user

        notifications = Notification.objects.filter(
            user=user
        ).order_by('-created_at')

        serializer = NotificationSerializer(notifications, many=True)

        return Response(serializer.data)
