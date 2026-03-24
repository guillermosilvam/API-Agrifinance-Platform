from rest_framework import viewsets
from .models import User, ProducerProfile, CompanyProfile
from .serializers import UserSerializer, ProducerProfileSerializer, CompanyProfileSerializer

# Create your views here.

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer