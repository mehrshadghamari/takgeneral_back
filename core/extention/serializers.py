from extention.models import Advertisement
from extention.models import Banner
from extention.models import Blog
from extention.models import BlogImage
from extention.models import BlogTag
from extention.models import Content
from extention.models import ContentImage
from extention.models import MainBanner
from extention.models import MetaTag
from extention.models import ProductClassification
from extention.models import Slider
from rest_framework import serializers


class SliderSerializer(serializers.ModelSerializer):
    mobile_image = serializers.SerializerMethodField('get_mobile_image_url')
    pc_image = serializers.SerializerMethodField('get_pc_image_url')

    class Meta:
        model = Slider
        fields = '__all__'

    def get_mobile_image_url(self, obj):
        request = self.context.get('request')
        mobile_image_url = obj.mobile_image.url
        return request.build_absolute_uri(mobile_image_url)

    def get_pc_image_url(self, obj):
        request = self.context.get('request')
        pc_image_url = obj.pc_image.url
        return request.build_absolute_uri(pc_image_url)


class ProductClassificationSerializer(serializers.ModelSerializer):
    product_image = serializers.SerializerMethodField('get_product_image_url')

    class Meta:
        model = ProductClassification
        fields = '__all__'

    def get_product_image_url(self, obj):
        request = self.context.get('request')
        product_image_url = obj.product_image.url
        return request.build_absolute_uri(product_image_url)


class AdvertisementSerilizer(serializers.ModelSerializer):
    mobile_image = serializers.SerializerMethodField('get_mobile_image_url')
    pc_image = serializers.SerializerMethodField('get_pc_image_url')

    class Meta:
        model = Advertisement
        fields = '__all__'

    def get_mobile_image_url(self, obj):
        request = self.context.get('request')
        mobile_image_url = obj.mobile_image.url
        return request.build_absolute_uri(mobile_image_url)

    def get_pc_image_url(self, obj):
        request = self.context.get('request')
        pc_image_url = obj.pc_image.url
        return request.build_absolute_uri(pc_image_url)


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model= Content
        fields = ("desc",)


class MetaTagSerializer(serializers.ModelSerializer):
    class Meta:
        model= MetaTag
        exclude = ("product","category","brand")


class MainBannerSAerializer(serializers.ModelSerializer):
    mobile_image = serializers.SerializerMethodField('get_mobile_image_url')
    image = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = MainBanner
        exclude = ("category","brand")

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
        exclude = ("category","brand")

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

    class Meta:
        model= Blog
        fields="__all__"


class AllBlogSerializer(serializers.ModelSerializer):
    main_image = BlogImageSerializer()
    tag = BlogTagSerializer(many=True)

    class Meta:
        model= Blog
        fields=("id","title","main_image","tag","create_time")
