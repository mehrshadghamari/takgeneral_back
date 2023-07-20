from django.contrib import admin
from extention.models import Advertisement
from extention.models import Content
from extention.models import ContentImage,Banner,MainBanner
from extention.models import ProductClassification
from extention.models import Slider
from nested_inline.admin import NestedModelAdmin
from nested_inline.admin import NestedTabularInline

admin.site.register(Slider)
admin.site.register(ProductClassification)
admin.site.register(Advertisement)



class MainBannerInline(NestedTabularInline):
    model=MainBanner
    fields =["mobile_image","image","alt","link_url"]
    extra=1



class BannerInline(NestedTabularInline):
    model=Banner
    fields = ["image","alt","link_url"]
    extra=2



class ContentImageInline(NestedTabularInline):
    model = ContentImage
    extra = 2

class ContentInline(NestedTabularInline):
    model = Content
    extra = 1
    fields = ["desc"]
    inlines = [ContentImageInline]


admin.site.register(MainBanner)
admin.site.register(Banner)



@admin.register(Content)
class ContenttAdmin(admin.ModelAdmin):
    # ...
    fields = ["url","desc",]
    inlines = [
        ContentImageInline,
    ]
