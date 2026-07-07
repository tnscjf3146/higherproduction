from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlanViewSet, PlanTypeViewSet, RecommendViewSet, OperationViewSet, ProductionViewSet, ItemViewSet

router = DefaultRouter()
router.register('plan_types', PlanTypeViewSet)
router.register('plans', PlanViewSet)
router.register('recommends', RecommendViewSet)
router.register('operations', OperationViewSet)
router.register('productions', ProductionViewSet)
router.register('items', ItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
