from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.


"""
Billing address model
"""


class BillingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=265, blank=True)
    postcode = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=45, blank=True)
    country = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.user.profile.username} Billing Address"

    def is_fully_filled(self):
        """
        Checks if all fields are complete
        """
        field_names = [f.name for f in self._meta.get_fields()]
        for field_name in field_names:
            value = getattr(self, field_name)
            if value is None or value == "":
                return False
        return True

    class Meta:
        verbose_name_plural = "Billing Address"
