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
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='producer_profile'
    )
    rif = models.CharField(max_length=20, unique=True)
    farm_name = models.CharField(max_length=100)
    address = models.TextField()
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
    is_verified_at = models.DateTimeField(null=True, blank=True)
    

    def __str__(self):
        return self.company_name