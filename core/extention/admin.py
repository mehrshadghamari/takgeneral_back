from django.contrib import admin
from extention.models import Advertisement
from extention.models import Content
from extention.models import ContentImage
from extention.models import ProductClassification
from extention.models import Slider

admin.site.register(Slider)
admin.site.register(ProductClassification)
admin.site.register(Advertisement)
# admin.site.register(Content)
# admin.site.register(PompBrand)
# admin.site.register(PompMain)
# admin.site.register(PompType)



class ContentImageInline(admin.TabularInline):
    model = ContentImage
    extra = 3

class ContentInline(admin.TabularInline):
    model = Content
    extra = 1
    fields = ["desc"]
    inlines = [ContentImageInline]


@admin.register(Content)
class ProductAdmin(admin.ModelAdmin):
    # ...
    fields = ["url","desc",]
    inlines = [
        ContentImageInline,
    ]
