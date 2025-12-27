from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'created_at')
    search_fields = ('name', 'phone')

from .models import ServiceJob

@admin.register(ServiceJob)
class ServiceJobAdmin(admin.ModelAdmin):
    list_display = ("customer", "device", "status", "estimated_cost", "created_at")
    list_filter = ("status",)
    search_fields = ("customer__name", "device")
