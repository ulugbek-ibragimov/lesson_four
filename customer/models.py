from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.

class Customer(User):
    gender = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=128)

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return self.phone_number
