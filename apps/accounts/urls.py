from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ProducerProfileViewSet, CompanyProfileViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'producer', ProducerProfileViewSet)
router.register(r'company', CompanyProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]