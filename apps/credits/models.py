from django.db import models
from apps.accounts.models import CompanyProfile, ProducerProfile

# Create your models here.

class CreditPlan(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='plans')
    title = models.CharField(max_length=100)
    description = models.TextField()
    agricultural_sector = models.CharField(max_length=100)
    min_amount = models.DecimalField(max_digits=12, decimal_places=2)
    max_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term_months = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.company.company_name}"
    
class CreditRequest(models.Model):
    producer = models.ForeignKey(ProducerProfile, on_delete=models.CASCADE, related_name='requests')
    credit_plan = models.ForeignKey(CreditPlan, on_delete=models.CASCADE, related_name='applications')
    application_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints =  [
            models.UniqueConstraint(
                fields=['producer', 'credit_plan'],
                name='unique_application_per_producer_per_plan'
            )
        ]
    
    def __str__(self):
        return f"Request by {self.producer.farm_name} for {self.credit_plan.title}"