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
        fields = ('schema')


class MetaTagSerializer(serializers.ModelSerializer):
    schemas = MetaTagSchemaSerializer(many=True)
    google_index = serializers.CharField()

    class Meta:
        model = MetaTag
        exclude = ("content_type", "object_id", "index", "follow")


class MainBannerSAerializer(serializers.ModelSerializer):
    mobile_image = serializers.SerializerMethodField('get_mobile_image_url')
    image = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = MainBanner
        exclude = ("content_type", "object_id")

    def get_mobile_image_url(self, obj):
        request = self.context.get('request')
        mobile_image_url = obj.mobile_image.url
        return request.build_absolute_uri(mobile_image_url)

    def get_image_url(self, obj):
        request = self.context.get('request')
        image_url = obj.image.url
        return request.build_absolute_uri(image_url)


class BannerSAerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = Banner
        exclude = ("content_type", "object_id")

    def get_image_url(self, obj):
        request = self.context.get('request')
        image_url = obj.image.url
        return request.build_absolute_uri(image_url)


class HomeMainBannerSerializer(serializers.ModelSerializer):
    mobile_image = serializers.SerializerMethodField('get_mobile_image_url')
    image = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = HomeMainBanner

    def get_mobile_image_url(self, obj):
        request = self.context.get('request')
        mobile_image_url = obj.mobile_image.url
        return request.build_absolute_uri(mobile_image_url)

    def get_image_url(self, obj):
        request = self.context.get('request')
        image_url = obj.image.url
        return request.build_absolute_uri(image_url)


class HomeBannerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = HomeBanner

    def get_image_url(self, obj):
        request = self.context.get('request')
        image_url = obj.image.url
        return request.build_absolute_uri(image_url)


class PopularHomeCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    products = AllProductSerializer(many=True)
    image = serializers.SerializerMethodField('get_image_url')

    def get_image_url(self, obj):
        request = self.context.get('request')
        image_url = obj.image.url
        return request.build_absolute_uri(image_url)

    class Meta:
        model = PopularHomeCategory
        fields = '__all__'


class BlogTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTag
        fields = "__all__"


class BlogImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image_url')

    def get_image_url(self, obj):
        request = self.context.get('request')
        image_url = obj.image.url
        return request.build_absolute_uri(image_url)

    class Meta:
        model = BlogImage
        fields = "__all__"


class BlogSerializer(serializers.ModelSerializer):
    blog_images = BlogImageSerializer(many=True)
    tag = BlogTagSerializer(many=True)
    created_time = serializers.SerializerMethodField()

    def get_created_time(self, obj):
        return {'date': obj.created_time.strftime('%Y-%m-%d'), 'time': obj.created_time.strftime('%H:%M:%S'),
                'timestamp': int(obj.created_time.timestamp())}

    class Meta:
        model = Blog
        fields = "__all__"


class AllBlogSerializer(serializers.ModelSerializer):
    main_image = BlogImageSerializer()
    tag = BlogTagSerializer(many=True)
    created_time = serializers.SerializerMethodField()

    def get_created_time(self, obj):
        return {'date': obj.created_time.strftime('%Y-%m-%d'), 'time': obj.created_time.strftime('%H:%M:%S'),
                'timestamp': int(obj.created_time.timestamp())}

    class Meta:
        model = Blog
        fields = ("id", "title", "main_image", "tag", "desc", "created_time")
