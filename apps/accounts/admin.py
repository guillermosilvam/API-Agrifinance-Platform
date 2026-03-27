from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import User, ProducerProfile, CompanyProfile

# Register your models here.

@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    list_display = ('username', 'email', 'is_producer', "is_company", 'is_staff')
    list_filter = ('is_producer', 'is_company')
    fieldsets = DefaultUserAdmin.fieldsets + (
        ('Role Information', {'fields': ('is_producer', 'is_company')}),
    )

@admin.register(ProducerProfile)
class ProducerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'farm_name', 'rif', 'created_at')
    search_fields = ('farm_name', 'rif', 'user__username')

@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'rif', 'status', 'is_verified_at')
    list_filter = ('status',)
    search_fields = ('company_name', 'rif', 'user__username')
    readonly_fields = ('is_verified_at',)