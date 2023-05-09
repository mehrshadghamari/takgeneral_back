from django.contrib import admin

# Register your models here.
from .models import Like,Comment,Reply

admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Like)