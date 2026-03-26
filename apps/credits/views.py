from rest_framework import viewsets, permissions
from .serializers import CreditPlanSerializer, CreditRequestSerializer
from .models import CreditPlan, CreditRequest
from drf_spectacular.utils import extend_schema, extend_schema_view
from .permissions import IsCompanyUser, IsProducerUser

@extend_schema(tags=['Credit Plans'])
@extend_schema_view(
    list=extend_schema(summary="List Credit Plans", description="Returns all active credit plans in the system."),
    create=extend_schema(summary="Create Credit Plan", description="Allows a company to publish a new financing plan."),
    retrieve=extend_schema(summary="Credit Plan Details", description="Retrieves full information for a specific credit plan."),
    update=extend_schema(summary="Update Credit Plan", description="Allows a company to modify an existing credit plan."),
    partial_update=extend_schema(summary="Partially Update Credit Plan", description="Allows a company to partially modify an existing credit plan."),
    destroy=extend_schema(summary="Delete Credit Plan", description="Allows a company to delete an existing credit plan.")
)
class CreditPlanViewSet(viewsets.ModelViewSet):
    queryset = CreditPlan.objects.filter(is_active=True, company__is_verified=True).order_by('-created_at')
    serializer_class = CreditPlanSerializer
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsCompanyUser()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company_profile)

@extend_schema(tags=['Credit Requests'])
@extend_schema_view(
    create=extend_schema(
        summary="Submit Credit Application",
        description="Creates an expression of interest between a producer and a plan. Note: duplicates are not allowed."
    ),
    list=extend_schema(summary="List Applications", description="Displays the system's intermediation history."),
    retrieve=extend_schema(summary="Application Details", description="Retrieves full information for a specific credit request."),
    update=extend_schema(summary="Update Application", description="Allows a producer to modify an existing credit request."),
    partial_update=extend_schema(summary="Partially Update Application", description="Allows a producer to partially modify an existing credit request."),
    destroy=extend_schema(summary="Delete Application", description="Allows a producer to delete an existing credit request.")
)
class CreditRequestViewSet(viewsets.ModelViewSet):
    queryset = CreditRequest.objects.all()
    serializer_class = CreditRequestSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsProducerUser()]
        return [permissions.IsAuthenticated()]
    
    def perform_create(self, serializer):
        serializer.save(producer=self.request.user.producer_profile)