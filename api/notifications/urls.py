from django.urls import path

from .views import NotificationListView

urlpattenrs = [

    path('notification/', NotificationListView.as_view(), name='notification')

]