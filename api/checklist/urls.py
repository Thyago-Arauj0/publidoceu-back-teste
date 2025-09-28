from django.urls import path, include
from rest_framework_nested import routers

from api.board.views import BoardViewSet

from .views import ChecklistViewSet

router = routers.SimpleRouter()
router.register(r'board', BoardViewSet, basename='board-checklist')

checklists_router = routers.NestedSimpleRouter(router, r'board', lookup='board')
checklists_router.register(r'checklist', ChecklistViewSet, basename='board-checklists')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(checklists_router.urls)),
]
