from rest_framework import serializers

from extention.models import Banner
from extention.models import Blog
from extention.models import BlogImage
from extention.models import BlogTag
from extention.models import Content
from extention.models import MainBanner
from extention.models import MetaTag


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ("desc",)


class MetaTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaTag
        exclude = ("product", "category", "brand")


class MainBannerSAerializer(serializers.ModelSerializer):
    mobile_image = serializers.SerializerMethodField('get_mobile_image_url')
    image = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = MainBanner
        exclude = ("category", "brand")

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
        exclude = ("category", "brand")

    def get_image_url(self, obj):
        request = self.context.get('request')
        image_url = obj.image.url
        return request.build_absolute_uri(image_url)


class BlogTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTag
        fields="__all__"


class BlogImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image_url')

    def get_image_url(self, obj):
        request = self.context.get('request')
        image_url = obj.image.url
        return request.build_absolute_uri(image_url)

    class Meta:
        model = BlogImage
        fields="__all__"

class BlogSerializer(serializers.ModelSerializer):
    blog_images = BlogImageSerializer(many=True)
    tag = BlogTagSerializer(many=True)
    created_time = serializers.SerializerMethodField()

    def get_created_time(self, obj):
        return {'date': obj.created_time.strftime('%Y-%m-%d'), 'time': obj.created_time.strftime('%H:%M:%S'), 'timestamp': int(obj.created_time.timestamp())}

    class Meta:
        model= Blog
        fields="__all__"


class AllBlogSerializer(serializers.ModelSerializer):
    main_image = BlogImageSerializer()
    tag = BlogTagSerializer(many=True)
    created_time = serializers.SerializerMethodField()

    def get_created_time(self, obj):
        return {'date': obj.created_time.strftime('%Y-%m-%d'), 'time': obj.created_time.strftime('%H:%M:%S'), 'timestamp': int(obj.created_time.timestamp())}

    class Meta:
        model= Blog
        fields=("id","title","main_image","tag","desc","created_time")