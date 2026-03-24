from django.contrib import admin
from .models import User, ProducerProfile, CompanyProfile

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_producer', "is_company", 'is_staff')
    list_filter = ('is_producer', 'is_company')

admin.site.register(ProducerProfile)
admin.site.register(CompanyProfile)