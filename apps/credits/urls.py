from .views import CreditPlanViewSet, CreditRequestViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'plans', CreditPlanViewSet)
router.register(r'applications', CreditRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
