from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Create your models here.
class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=9, unique=True)
    address = models.TextField()
    zip_code = models.CharField(max_length=6)
    rodo = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username