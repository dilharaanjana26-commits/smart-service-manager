from django import forms
from .models import Customer
from .models import ServiceJob

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "phone", "email", "address"]

class ServiceJobForm(forms.ModelForm):
    class Meta:
        model = ServiceJob
        fields = ["customer", "device", "problem", "estimated_cost"]