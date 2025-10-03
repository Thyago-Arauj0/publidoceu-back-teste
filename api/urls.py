from django.urls import path, include

urlpatterns = [

    path('', include('api.board.urls')),
    path('auth/', include('api.auth.urls')),
    path('', include('api.card.urls')),
    path('', include('api.checklist.urls')),
    path('', include('api.notifications.urls')),
    path('', include('api.file.urls')), 

]