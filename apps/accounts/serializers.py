from rest_framework import serializers
from django.db import transaction
from .models import User, ProducerProfile, CompanyProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_producer', 'is_company']
        extra_kwargs = {'password': {'write_only': True}}


class ProducerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ProducerProfile
        fields = '__all__'

class CompanyProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = CompanyProfile
        fields = '__all__'

class ProducerRegisterSerializer(serializers.ModelSerializer):
    # Definición de campos adicionales
    farm_name = serializers.CharField(max_length=100, write_only=True)
    address = serializers.CharField(write_only=True)
    rif = serializers.CharField(max_length=20, required=False, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'farm_name', 'address', 'rif']
        # ESTA ES LA CLAVE: Marca los campos como solo escritura
        extra_kwargs = {
            'password': {'write_only': True},
        }

    @transaction.atomic
    def create(self, validated_data):
        farm_name = validated_data.pop('farm_name')
        address = validated_data.pop('address')
        rif = validated_data.pop('rif', None)
        
        user = User.objects.create_user(is_producer=True, is_company=False, **validated_data)
        
        # Se crea el perfil vinculado al usuario en PostgreSQL
        ProducerProfile.objects.create(
            user=user,
            farm_name=farm_name,
            address=address,
            rif=rif if rif else f"TEMP-P-{user.id}"
        )
        return user

class CompanyRegisterSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(max_length=150, write_only=True)
    rif = serializers.CharField(max_length=20, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'company_name', 'rif']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    @transaction.atomic
    def create(self, validated_data):
        company_name = validated_data.pop('company_name')
        rif = validated_data.pop('rif')
        
        user = User.objects.create_user(is_producer=False, is_company=True, **validated_data)
        
        # El campo is_verified queda en False por defecto para aprobación del admin
        CompanyProfile.objects.create(
            user=user,
            company_name=company_name,
            rif=rif
        )
        return user