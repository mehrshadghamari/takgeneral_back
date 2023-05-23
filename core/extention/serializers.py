from extention.models import Advertisement
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
