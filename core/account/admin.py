from django.contrib import admin

from django.contrib import admin


from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from doctors.forms import UserAdminCreationForm, UserAdminChangeForm



User = get_user_model()

admin.site.register(User)
