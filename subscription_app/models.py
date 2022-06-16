from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

# Model to support Subscriptions
class CustomerStatus(models.Model):
    STATUSES = [
        ('active', 'active'),
        ('pause', 'pause'),
    ]

    status = models.CharField(max_length=15, choices=STATUSES, unique=True)

    def __str__(self):
        return self.status


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripeid = models.CharField(max_length=255)
    stripe_subscription_id = models.CharField(max_length=255)
    cancel_at_period_end = models.BooleanField(default=False)
    membership = models.BooleanField(default=False)
    status = models.ForeignKey(CustomerStatus, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.user)



