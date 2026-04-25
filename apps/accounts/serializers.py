from rest_framework import serializers
from django.db import transaction
from .models import User, ProducerProfile, CompanyProfile
from django.utils import timezone
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class BaseProducerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProducerProfile
        exclude = ['user']

class BaseCompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        exclude = ['user']

class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_producer', 'is_company', 'profile']
        extra_kwargs = {'password': {'write_only': True}}
        
    def get_profile(self, obj):
        if obj.is_producer and hasattr(obj, 'producerprofile'):
            return BaseProducerProfileSerializer(obj.producerprofile).data
        elif obj.is_company and hasattr(obj, 'companyprofile'):
            return BaseCompanyProfileSerializer(obj.companyprofile).data
        return None


class ProducerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ProducerProfile
        fields = '__all__'

    def validate(self, data):
        total_area = data.get('total_area')
        cultivated_area = data.get('cultivated_area')
        
        if self.instance:
            total_area = total_area if total_area is not None else self.instance.total_area
            cultivated_area = cultivated_area if cultivated_area is not None else self.instance.cultivated_area

        if total_area is not None and cultivated_area is not None:
            if cultivated_area > total_area:
                raise serializers.ValidationError({
                    "cultivated_area": "Cultivated area cannot be strictly greater than total area."
                })
        return data

class CompanyProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = CompanyProfile
        fields = '__all__'
        read_only_fields = ['status', 'is_verified_at']

    def validate_corporate_phone(self, value):
        if value:
            # Basic validation for phone number
            clean_value = value.replace('+', '').replace('-', '').replace(' ', '')
            if not clean_value.isdigit():
                raise serializers.ValidationError("Phone number must contain only digits and valid separators (+, -, spaces).")
        return value

class ProducerRegisterSerializer(serializers.ModelSerializer):
    farm_name = serializers.CharField(max_length=150, write_only=True)
    address = serializers.CharField(write_only=True)
    rif = serializers.CharField(max_length=20, required=False, write_only=True)
    
    # New Fields
    national_id = serializers.CharField(max_length=20, required=False, write_only=True)
    phone_number = serializers.CharField(max_length=20, required=False, write_only=True)
    total_area = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, write_only=True)
    cultivated_area = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, write_only=True)
    land_tenure = serializers.CharField(max_length=20, required=False, write_only=True)
    machinery_inventory = serializers.CharField(required=False, write_only=True)
    road_condition = serializers.CharField(max_length=20, required=False, write_only=True)
    main_activity = serializers.CharField(max_length=100, required=False, write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'farm_name', 'address', 'rif',
            'national_id', 'phone_number', 'total_area', 'cultivated_area',
            'land_tenure', 'machinery_inventory', 'road_condition', 'main_activity'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    @transaction.atomic
    def create(self, validated_data):
        # Extract profiles fields
        profile_data = {
            'farm_name': validated_data.pop('farm_name', ''),
            'address': validated_data.pop('address', ''),
            'rif': validated_data.pop('rif', None),
            'national_id': validated_data.pop('national_id', None),
            'phone_number': validated_data.pop('phone_number', None),
            'total_area': validated_data.pop('total_area', None),
            'cultivated_area': validated_data.pop('cultivated_area', None),
            'land_tenure': validated_data.pop('land_tenure', None),
            'machinery_inventory': validated_data.pop('machinery_inventory', None),
            'road_condition': validated_data.pop('road_condition', None),
            'main_activity': validated_data.pop('main_activity', None),
        }
        
        user = User.objects.create_user(is_producer=True, is_company=False, **validated_data)
        
        # Ensure RIF
        if not profile_data['rif']:
            profile_data['rif'] = f"TEMP-P-{user.id}"
            
        ProducerProfile.objects.create(user=user, **profile_data)
        return user

class CompanyRegisterSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(max_length=150, write_only=True)
    rif = serializers.CharField(max_length=20, write_only=True)

    # New Fields
    legal_name = serializers.CharField(max_length=200, required=False, write_only=True)
    corporate_phone = serializers.CharField(max_length=20, required=False, write_only=True)
    website = serializers.URLField(required=False, write_only=True)
    fiscal_address = serializers.CharField(required=False, write_only=True)
    company_type = serializers.CharField(max_length=20, required=False, write_only=True)
    description = serializers.CharField(required=False, write_only=True)
    response_time = serializers.CharField(max_length=50, required=False, write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'company_name', 'rif',
            'legal_name', 'corporate_phone', 'website', 'fiscal_address',
            'company_type', 'description', 'response_time'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    @transaction.atomic
    def create(self, validated_data):
        profile_data = {
            'company_name': validated_data.pop('company_name'),
            'rif': validated_data.pop('rif'),
            'legal_name': validated_data.pop('legal_name', None),
            'corporate_phone': validated_data.pop('corporate_phone', None),
            'website': validated_data.pop('website', None),
            'fiscal_address': validated_data.pop('fiscal_address', None),
            'company_type': validated_data.pop('company_type', None),
            'description': validated_data.pop('description', None),
            'response_time': validated_data.pop('response_time', None),
        }
        
        user = User.objects.create_user(is_producer=False, is_company=True, **validated_data)
        
        # El campo status queda en 'pending' por defecto para aprobación del admin
        CompanyProfile.objects.create(user=user, **profile_data)
        return user

class CompanyVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = ['status', 'is_verified_at']
        read_only_fields = ['is_verified_at']

    def update(self, instance, validated_data):
        new_status = validated_data.get('status')
        instance.status = new_status

        if new_status == CompanyProfile.VERIFIED:
            instance.is_verified_at = timezone.now()
        else:
            instance.is_verified_at = None
        instance.save()
        return instance

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Determinar rol dinamico para frontend (Next.js)
        role = 'admin'
        if self.user.is_company:
            role = 'company'
        elif self.user.is_producer:
            role = 'producer'
        elif self.user.is_superuser or self.user.is_staff:
            role = 'admin'
            
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'role': role
        }
        return data