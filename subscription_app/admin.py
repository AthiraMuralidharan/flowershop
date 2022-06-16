from django.contrib import admin
from subscription_app.models import Customer, CustomerStatus
# Register your models here.


admin.site.register(Customer)
admin.site.register(CustomerStatus)