from django.contrib import admin

# Register your models here.
from .models import Order
from .models import OrderItem

admin.site.register(Order)
admin.site.register(OrderItem)
