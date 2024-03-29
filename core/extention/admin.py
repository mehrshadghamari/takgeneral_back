from django.contrib import admin
from extention.models import Banner
from extention.models import Blog
from extention.models import BlogImage
from extention.models import BlogTag
from extention.models import Content
from extention.models import ContentImage
from extention.models import HomeBanner
from extention.models import HomeMainBanner
from extention.models import MainBanner
from extention.models import MetaTag
from extention.models import MetaTagSchema
from extention.models import PopularHomeCategory
from nested_inline.admin import NestedModelAdmin
from nested_inline.admin import NestedStackedInline
from nested_inline.admin import NestedTabularInline

admin.site.register(MainBanner)
admin.site.register(Banner)
admin.site.register(HomeMainBanner)
admin.site.register(HomeBanner)
admin.site.register(BlogTag)


class PopularHomeCategoryInline(NestedTabularInline):
    model = PopularHomeCategory
    extra = 1


class BlogInline(NestedTabularInline):
    model = BlogImage
    extra = 1


class MainBannerInline(NestedTabularInline):
    model = MainBanner
    fields = ["mobile_image", "image", "alt", "link_url"]
    extra = 1


class BannerInline(NestedTabularInline):
    model = Banner
    fields = ["image", "alt", "link_url"]
    extra = 2


class MetaTagSchemaInline(NestedTabularInline):
    model = MetaTagSchema
    extra = 1


class MetaTagInline(NestedStackedInline):
    model = MetaTag
    inlines = [MetaTagSchemaInline]

    fields = ("title",
              "desc",
              "og_title",
              "og_desc",
              "og_type",
              "og_url",
              "og_locale",
              "og_site_name",
              "canonical",
              "follow",
              "index",
              "og_image",
              "twiter_cart",)
    extra = 1


class ContentImageInline(NestedTabularInline):
    model = ContentImage
    extra = 2


class ContentInline(NestedTabularInline):
    model = Content
    extra = 1
    fields = ["desc"]
    inlines = [ContentImageInline]


@admin.register(Blog)
class BlogAdmin(NestedModelAdmin):
    inlines = [BlogInline, ]
    filter_horizontal = ["tag"]


@admin.register(Content)
class ContenttAdmin(admin.ModelAdmin):
    # ...
    fields = ["url", "desc", ]
    inlines = [
        ContentImageInline,
    ]
