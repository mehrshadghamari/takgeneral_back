from extention.models import Banner
from extention.models import Content
from extention.models import ContentImage
from extention.models import MainBanner
from extention.models import MetaTag

from rest_framework import serializers




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
