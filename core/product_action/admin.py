from django.contrib import admin

# Register your models here.
from .models import CommentLike,Comment,Reply

admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(CommentLike)