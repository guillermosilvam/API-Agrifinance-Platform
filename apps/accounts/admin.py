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

admin.site.register(ProducerProfile)
admin.site.register(CompanyProfile)