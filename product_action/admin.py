from django.contrib import admin

# Register your models here.
from .models import Comment
from .models import CommentLike
from .models import Question
from .models import Reply

admin.site.register(Comment)
admin.site.register(CommentLike)
admin.site.register(Question)
admin.site.register(Reply)
