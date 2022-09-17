from django import forms
from dataclasses import fields
from .models import BillingAddress


class BillingAddressForm(forms.ModelForm):
    """
    Billing address form when checking out
    """

    class Meta:
        model = BillingAddress
        fields = ["address", "postcode", "city", "country"]
