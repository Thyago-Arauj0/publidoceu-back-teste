from django.urls import path, include
from rest_framework_nested import routers

from api.board.views import BoardViewSet
from api.card.views import CardViewset
from api.file.views import FileCardViewSet

router = routers.SimpleRouter()
router.register(r'board', BoardViewSet, basename='board')

cards_router = routers.NestedSimpleRouter(router, r'board', lookup='board')
cards_router.register(r'card', CardViewset, basename='board-card')

files_router = routers.NestedSimpleRouter(cards_router, r'card', lookup='card')
files_router.register(r'files', FileCardViewSet, basename='card-files')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(cards_router.urls)),
    path('', include(files_router.urls)),
]
