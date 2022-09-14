from django import forms
from dataclasses import fields
from .models import BillingAddress

"""
Billing address form when checking out
"""
class BillingAddressForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = ['address', 'postcode', 'city', 'country']