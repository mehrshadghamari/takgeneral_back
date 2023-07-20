from django.contrib import admin
from extention.models import Advertisement
from extention.models import Content
from extention.models import ContentImage
from extention.models import ProductClassification
from extention.models import Slider
from nested_inline.admin import NestedModelAdmin
from nested_inline.admin import NestedTabularInline

admin.site.register(Slider)
admin.site.register(ProductClassification)
admin.site.register(Advertisement)
# admin.site.register(Content)
# admin.site.register(PompBrand)
# admin.site.register(PompMain)
# admin.site.register(PompType)



class ContentImageInline(NestedTabularInline):
    model = ContentImage
    extra = 2

class ContentInline(NestedTabularInline):
    model = Content
    extra = 1
    fields = ["desc"]
    inlines = [ContentImageInline]


@admin.register(Content)
class ContenttAdmin(admin.ModelAdmin):
    # ...
    fields = ["url","desc",]
    inlines = [
        ContentImageInline,
    ]
