from rest_framework import viewsets
from .models import User, ProducerProfile, CompanyProfile
from .serializers import UserSerializer, ProducerProfileSerializer, CompanyProfileSerializer

# Create your views here.

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class ProducerProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing producer profiles.
    """
    queryset = ProducerProfile.objects.all()
    serializer_class = ProducerProfileSerializer

class CompanyProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing company profiles.
    """
    queryset = CompanyProfile.objects.all()
    serializer_class = CompanyProfileSerializer