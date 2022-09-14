from django.db import models

from django.contrib.auth.models import User


"""
Model for inputting user details
"""
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(default='default.png', upload_to='profile_images')
    bio = models.TextField(blank=True, null=True)
    full_name = models.CharField(max_length=265, blank=True)
    address_1 = models.TextField(max_length=300, blank=True)
    country = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    post_code = models.CharField(max_length=12, blank=True)


    def __str__(self):
        return self.user.username

    def is_fully_filled(self):
        fields_names = [f.name for f in self._meta.get_fields()]
        for field_name in fields_names:
            value = getattr(self, field_name)
            if value is None or value =='':
                return False
        return True

