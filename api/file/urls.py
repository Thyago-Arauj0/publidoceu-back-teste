from django.urls import path, include
from rest_framework_nested import routers

from api.card.views import CardViewset
from api.file.views import FileCardViewSet

# Router principal do Card
router = routers.SimpleRouter()
router.register(r'card', CardViewset, basename='card')

# Router aninhado para Files
files_router = routers.NestedSimpleRouter(router, r'card', lookup='card')
files_router.register(r'files', FileCardViewSet, basename='card-files')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(files_router.urls)),
]
