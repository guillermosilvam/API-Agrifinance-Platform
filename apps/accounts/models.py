from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    """
    Custom User model to handle role-based access control
    """
    is_producer = models.BooleanField('Producer status', default=False)
    is_company = models.BooleanField('Company/Bank status', default=False)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class ProducerProfile(models.Model):
    TENURE_CHOICES = [
        ('OWNED', 'Owned'),
        ('RENTED', 'Rented'),
        ('AWARDED', 'Awarded'),
    ]
    ROAD_CONDITION_CHOICES = [
        ('OPTIMAL', 'Optimal'),
        ('REGULAR', 'Regular'),
        ('DIFFICULT', 'Difficult'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='producer_profile'
    )
    rif = models.CharField(max_length=20, unique=True)
    farm_name = models.CharField(max_length=150, verbose_name="Farm Name")
    address = models.TextField()
    national_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    total_area = models.DecimalField(max_digits=10, decimal_places=2, help_text="Total hectares", null=True, blank=True)
    cultivated_area = models.DecimalField(max_digits=10, decimal_places=2, help_text="Active hectares", null=True, blank=True)
    land_tenure = models.CharField(max_length=20, choices=TENURE_CHOICES, null=True, blank=True)
    machinery_inventory = models.TextField(help_text="Description of tractors, equipment, etc.", null=True, blank=True)
    road_condition = models.CharField(max_length=20, choices=ROAD_CONDITION_CHOICES, null=True, blank=True)
    main_activity = models.CharField(max_length=100, help_text="Ex: Corn, Cattle, etc.", null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.farm_name} ({self.user.username})"
    
class CompanyProfile(models.Model):
    PENDING = 'pending'
    VERIFIED = 'verified'
    REJECTED = 'rejected'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (VERIFIED, 'Verified'),
        (REJECTED, 'Rejected'),
    ]

    COMPANY_TYPE_CHOICES = [
        ('BANK', 'Bank'),
        ('PRIVATE_FUND', 'Private Fund'),
        ('COOPERATIVE', 'Cooperative'),
        ('INVESTOR', 'Investor'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='company_profile'
    )
    rif = models.CharField(max_length=20, unique=True)
    company_name = models.CharField(max_length=150)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING
    )
    legal_name = models.CharField(max_length=200, help_text="Full legal name", null=True, blank=True)
    corporate_phone = models.CharField(max_length=20, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    fiscal_address = models.TextField(null=True, blank=True)
    company_type = models.CharField(max_length=20, choices=COMPANY_TYPE_CHOICES, null=True, blank=True)
    description = models.TextField(help_text="Brief 'About us' review", null=True, blank=True)
    response_time = models.CharField(max_length=50, help_text="Ex: 5 business days", null=True, blank=True)

    is_verified_at = models.DateTimeField(null=True, blank=True)
    

    def __str__(self):
        return self.company_name