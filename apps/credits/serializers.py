from rest_framework import serializers
from .models import CreditPlan, CreditRequest
from apps.accounts.serializers import ProducerProfileSerializer

class CreditPlanSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.company_name', read_only=True)

    class Meta:
        model = CreditPlan
        fields = [
            'id', 'company_name', 'title', 'description', 
            'agricultural_sector', 'min_amount', 'max_amount', 
            'interest_rate', 'term_months', 'is_active'
        ]

    def validate(self, data):
        min_amount = data.get('min_amount')
        max_amount = data.get('max_amount')

        if self.instance:
            min_amount = min_amount if min_amount is not None else self.instance.min_amount
            max_amount = max_amount if max_amount is not None else self.instance.max_amount

        if min_amount is not None and min_amount <= 0:
            raise serializers.ValidationError({"min_amount": "Minimum amount must be strictly positive."})

        if min_amount is not None and max_amount is not None:
            if min_amount >= max_amount:
                raise serializers.ValidationError({
                    "max_amount": "Maximum amount must be strictly greater than minimum amount."
                })
        
        return data

class CreditRequestSerializer(serializers.ModelSerializer):
    producer_profile = ProducerProfileSerializer(source='producer', read_only=True)
    credit_plan_title = serializers.CharField(source='credit_plan.title', read_only=True)

    class Meta:
        model = CreditRequest
        fields = ['id', 'producer', 'producer_profile', 'credit_plan', 'credit_plan_title', 'application_date']
        read_only_fields = ['producer', 'application_date']