from django.contrib import admin
from django.contrib.auth import get_user_model

# from doctors.forms import UserAdminCreationForm, UserAdminChangeForm
from .models import Address

User = get_user_model()

admin.site.register(User)
admin.site.register(Address)
