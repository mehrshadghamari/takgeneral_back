from extention.models import Banner
from extention.models import Blog
from extention.models import BlogImage
from extention.models import BlogTag
from extention.models import Content
from extention.models import HomeBanner
from extention.models import HomeMainBanner
from extention.models import MainBanner
from extention.models import MetaTag
from extention.models import MetaTagSchema
from extention.models import PopularHomeCategory
from extention.models import Redirect
from product.models import Category
from product.models import Product
from product.models import ProductBrand
from product.serializers import AllProductSerializer
from product.serializers import CategorySerializer
from rest_framework import serializers


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ("desc",)


class MetaTagSchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaTagSchema
        fields = ("schema",)


class MetaTagSerializer(serializers.ModelSerializer):
    schemas = MetaTagSchemaSerializer(many=True)
    google_index = serializers.CharField()
    og_image = serializers.SerializerMethodField("get_og_image_url")
    twiter_image = serializers.SerializerMethodField("get_twiter_image_url")

    def get_og_image_url(self, obj):
        request = self.context.get("request")
        if obj.og_image:
            image_url = request.build_absolute_uri(obj.og_image.url)
        else:
            image_url = ""

        return image_url

    def get_twiter_image_url(self, obj):
        request = self.context.get("request")
        if obj.twiter_image:
            image_url = request.build_absolute_uri(obj.twiter_image.url)
        else:
            image_url = ""

        return image_url

    class Meta:
        model = MetaTag
        exclude = (
            "content_type",
            "object_id",
        )


class MainBannerSAerializer(serializers.ModelSerializer):
    mobile_image = serializers.SerializerMethodField("get_mobile_image_url")
    image = serializers.SerializerMethodField("get_image_url")

    class Meta:
        model = MainBanner
        exclude = (
            "content_type",
            "object_id",
        )

    def get_mobile_image_url(self, obj):
        request = self.context.get("request")
        mobile_image_url = obj.mobile_image.url
        return request.build_absolute_uri(mobile_image_url)

    def get_image_url(self, obj):
        request = self.context.get("request")
        image_url = obj.image.url
        return request.build_absolute_uri(image_url)


class BannerSAerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField("get_image_url")

    class Meta:
        model = Banner
        exclude = (
            "content_type",
            "object_id",
        )

    def get_image_url(self, obj):
        request = self.context.get("request")
        image_url = obj.image.url
        return request.build_absolute_uri(image_url)


class HomeMainBannerSerializer(serializers.ModelSerializer):
    mobile_image = serializers.SerializerMethodField("get_mobile_image_url")
    image = serializers.SerializerMethodField("get_image_url")

    class Meta:
        model = HomeMainBanner
        fields = "__all__"

    def get_mobile_image_url(self, obj):
        request = self.context.get("request")
        mobile_image_url = obj.mobile_image.url
        return request.build_absolute_uri(mobile_image_url)

    def get_image_url(self, obj):
        request = self.context.get("request")
        image_url = obj.image.url
        return request.build_absolute_uri(image_url)


class HomeBannerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField("get_image_url")

    class Meta:
        model = HomeBanner
        fields = "__all__"

    def get_image_url(self, obj):
        request = self.context.get("request")
        image_url = obj.image.url
        return request.build_absolute_uri(image_url)


class PopularHomeCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    products = AllProductSerializer(many=True)
    image = serializers.SerializerMethodField("get_image_url")

    def get_image_url(self, obj):
        request = self.context.get("request")
        image_url = obj.image.url
        return request.build_absolute_uri(image_url)

    class Meta:
        model = PopularHomeCategory
        fields = "__all__"


class BlogTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTag
        fields = "__all__"


class BlogImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField("get_image_url")

    def get_image_url(self, obj):
        request = self.context.get("request")
        image_url = obj.image.url
        return request.build_absolute_uri(image_url)

    class Meta:
        model = BlogImage
        fields = "__all__"


class BlogSerializer(serializers.ModelSerializer):
    blog_images = BlogImageSerializer(many=True)
    tag = BlogTagSerializer(many=True)
    created_time = serializers.SerializerMethodField()
    updated_time = serializers.SerializerMethodField()

    def get_created_time(self, obj):
        return {
            "date": obj.created_time.strftime("%Y-%m-%d"),
            "time": obj.created_time.strftime("%H:%M:%S"),
            "timestamp": int(obj.created_time.timestamp()),
        }

    def get_updated_time(self, obj):
        return {
            "date": obj.updated_time.strftime("%Y-%m-%d"),
            "time": obj.updated_time.strftime("%H:%M:%S"),
            "timestamp": int(obj.updated_time.timestamp()),
        }

    class Meta:
        model = Blog
        fields = "__all__"


class AllBlogSerializer(serializers.ModelSerializer):
    main_image = BlogImageSerializer()
    blog_images = BlogImageSerializer(many=True)
    tag = BlogTagSerializer(many=True)
    created_time = serializers.SerializerMethodField()
    updated_time = serializers.SerializerMethodField()

    def get_created_time(self, obj):
        return {
            "date": obj.created_time.strftime("%Y-%m-%d"),
            "time": obj.created_time.strftime("%H:%M:%S"),
            "timestamp": int(obj.created_time.timestamp()),
        }

    def get_updated_time(self, obj):
        return {
            "date": obj.updated_time.strftime("%Y-%m-%d"),
            "time": obj.updated_time.strftime("%H:%M:%S"),
            "timestamp": int(obj.updated_time.timestamp()),
        }

    class Meta:
        model = Blog
        fields = (
            "id",
            "slug",
            "title",
            "main_image",
            "blog_images",
            "tag",
            "desc",
            "created_time",
            "updated_time",
        )


class RedirectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Redirect
        fields = "__all__"


class ProductSiteMapSerializer(serializers.ModelSerializer):
    update_at = serializers.SerializerMethodField()
    index= serializers.SerializerMethodField()

    def get_index(self,obj):
        return obj.meta_tag.first().index

    def get_update_at(self, obj):
        if obj.update_at:
            return {
                "date": obj.update_at.strftime("%Y-%m-%d"),
                "time": obj.update_at.strftime("%H:%M:%S"),
                "timestamp": int(obj.update_at.timestamp()),
            }

    class Meta:
        model = Product
        fields = (
            "id",
            "url",
            "update_at",
            "index",
        )


class BrandSiteMapSerializer(serializers.ModelSerializer):
    update_at = serializers.SerializerMethodField()
    index= serializers.SerializerMethodField()

    def get_index(self,obj):
        return obj.meta_tag.first().index

    def get_update_at(self, obj):
        if obj.update_at:
            return {
                "date": obj.update_at.strftime("%Y-%m-%d"),
                "time": obj.update_at.strftime("%H:%M:%S"),
                "timestamp": int(obj.update_at.timestamp()),
            }

    class Meta:
        model = ProductBrand
        fields = (
            "id",
            "url",
            "update_at",
            "index",
        )


class CategorySiteMapSerializer(serializers.ModelSerializer):
    update_at = serializers.SerializerMethodField()
    index= serializers.SerializerMethodField()

    def get_index(self,obj):
        return obj.meta_tag.first().index

    def get_update_at(self, obj):
        if obj.update_at:
            return {
                "date": obj.update_at.strftime("%Y-%m-%d"),
                "time": obj.update_at.strftime("%H:%M:%S"),
                "timestamp": int(obj.update_at.timestamp()),
            }

    class Meta:
        model = Category
        fields = (
            "id",
            "url",
            "update_at",
            "index",
        )


class BlogSiteMapSerializer(serializers.ModelSerializer):
    updated_time = serializers.SerializerMethodField()
    index= serializers.SerializerMethodField()

    def get_index(self,obj):
        return obj.meta_tag.first().index

    def get_updated_time(self, obj):
        if obj.updated_time:
            return {
                "date": obj.updated_time.strftime("%Y-%m-%d"),
                "time": obj.updated_time.strftime("%H:%M:%S"),
                "timestamp": int(obj.updated_time.timestamp()),
            }

    class Meta:
        model = Blog
        fields = (
            "id",
            "slug",
            "updated_time",
            "index",
        )


class SiteMapSerializer(serializers.Serializer):
    products = ProductSiteMapSerializer(many=True)
    brands = BrandSiteMapSerializer(many=True)
    categories = CategorySiteMapSerializer(many=True)
    blogs = BlogSiteMapSerializer(many=True)
