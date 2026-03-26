from rest_framework import viewsets, status, generics, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import User, ProducerProfile, CompanyProfile
from .serializers import UserSerializer, ProducerProfileSerializer, CompanyProfileSerializer, CompanyRegisterSerializer, ProducerRegisterSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema(tags=['Accounts'])
@extend_schema_view(
    list=extend_schema(summary="List Users", description="Returns all user accounts ordered by registration date."),
    retrieve=extend_schema(summary="User Detail", description="Retrieves full details for a specific user account."),
)
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

@extend_schema(tags=['Producer Accounts'])
@extend_schema_view(
    list=extend_schema(summary="List Producer Profiles", description="Returns all producer profiles."),
    create=extend_schema(summary="Create Producer Profile", description="Creates a new producer profile."),
    retrieve=extend_schema(summary="Producer Profile Detail", description="Retrieves full details for a specific producer profile."),
    update=extend_schema(summary="Update Producer Profile", description="Updates an existing producer profile."),
    partial_update=extend_schema(summary="Partially Update Producer Profile", description="Applies partial update to an existing producer profile."),
    destroy=extend_schema(summary="Delete Producer Profile", description="Deletes an existing producer profile."),
)
class ProducerProfileViewSet(viewsets.ModelViewSet):
    queryset = ProducerProfile.objects.all()
    serializer_class = ProducerProfileSerializer

@extend_schema(tags=['Company Accounts'])
@extend_schema_view(
    list=extend_schema(summary="List Company Profiles", description="Returns all company profiles."),
    create=extend_schema(summary="Create Company Profile", description="Creates a new company profile."),
    retrieve=extend_schema(summary="Company Profile Detail", description="Retrieves full details for a specific company profile."),
    update=extend_schema(summary="Update Company Profile", description="Updates an existing company profile."),
    partial_update=extend_schema(summary="Partially Update Company Profile", description="Applies partial update to an existing company profile."),
    destroy=extend_schema(summary="Delete Company Profile", description="Deletes an existing company profile."),
)
class CompanyProfileViewSet(viewsets.ModelViewSet):
    queryset = CompanyProfile.objects.all()
    serializer_class = CompanyProfileSerializer

def perform_create(self, serializer):
    serializer.save(producer=self.request.user.producer_profile)

@extend_schema(tags=['Producer Registration'])
class ProducerRegisterView(generics.CreateAPIView):
    serializer_class = ProducerRegisterSerializer
    permission_classes = [AllowAny]

@extend_schema(tags=['Company Registration'])
class CompanyRegisterView(generics.CreateAPIView):
    serializer_class = CompanyRegisterSerializer
    permission_classes = [AllowAny]