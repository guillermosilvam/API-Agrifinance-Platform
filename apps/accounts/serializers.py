from rest_framework import serializers
from .models import User, ProducerProfile, CompanyProfile

class UserSerializer(serializers.ModelSerializer):
    """
    Base user model for general information
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_producer', 'is_company']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

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
