from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ProducerProfileViewSet, CompanyProfileViewSet, ProducerRegisterView, CompanyRegisterView, CompanyReviewView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'producer', ProducerProfileViewSet)
router.register(r'company', CompanyProfileViewSet)

urlpatterns = [
    path('company/<int:pk>/review/', CompanyReviewView.as_view(), name='company-review'),
    path('', include(router.urls)),
    path('register/producer/', ProducerRegisterView.as_view(), name='producer-register'),
    path('register/company/', CompanyRegisterView.as_view(), name='company-register'),
]