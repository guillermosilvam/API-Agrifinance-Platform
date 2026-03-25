from rest_framework import serializers
from .models import CreditPlan, CreditRequest

class CreditPlanSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.company_name', read_only=True)

    class Meta:
        model = CreditPlan
        fields = [
            'id', 'company_name', 'title', 'description', 
            'agricultural_sector', 'min_amount', 'max_amount', 
            'interest_rate', 'term_months', 'is_active'
        ]

class CreditRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditRequest
        fields = ['id', 'producer', 'credit_plan', 'application_date']
        read_only_fields = ['application_date']