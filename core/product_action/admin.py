from django.contrib import admin

# Register your models here.
from .models import CommentLike,Comment,Reply,Question

admin.site.register(Comment)
admin.site.register(CommentLike)
admin.site.register(Question)
admin.site.register(Reply)