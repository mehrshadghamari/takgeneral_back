from rest_framework import serializers

from order.models import OrderItem
from product.models import ProductVariant
from product.serializers import productImagesSerializer


class OrderlistSerializer(serializers.ModelSerializer):
    price = serializers.IntegerField()
    final_price = serializers.IntegerField()
    sum_price = serializers.IntegerField()
    sum_final_price = serializers.IntegerField()
    sum_discount_price = serializers.IntegerField()
    quantity = serializers.IntegerField()
    warranty = serializers.CharField()
    product_id = serializers.IntegerField()
    name = serializers.CharField(source='product_name')
    main_image = productImagesSerializer(source='product_main_image', allow_null=True)
    product_variant_id = serializers.IntegerField(source='id')
    product_variant_key = serializers.SerializerMethodField("get_product_variant_key")
    product_variant_value = serializers.CharField(source='option_value')

    def get_product_variant_key(self, obj):
        return obj.option.name

    class Meta:
        model = ProductVariant
        fields = (
            'product_id', 'name', 'product_variant_id', 'product_variant_key', 'product_variant_value', 'main_image',
            'discount', 'seven_days_back', 'free_send', 'warranty',
            'quantity', 'price', 'final_price', 'sum_price', 'sum_final_price', 'sum_discount_price',)


class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.product_id')
    name = serializers.CharField(source='product.product_name')
    main_image = productImagesSerializer(
        source='product.product_main_image', allow_null=True)
    discount = serializers.IntegerField(source='product.discount')
    seven_days_back = serializers.BooleanField(
        source='product.seven_days_back')
    free_send = serializers.BooleanField(source='product.free_send')
    warranty = serializers.CharField(source='product.warranty')
    price = serializers.FloatField(source='product.price')
    final_price = serializers.SerializerMethodField()
    sum_price = serializers.ReadOnlyField()
    sum_final_price = serializers.ReadOnlyField()
    sum_discount_price = serializers.ReadOnlyField()
    product_variant_id = serializers.IntegerField(source='product.id')
    product_variant_key = serializers.SerializerMethodField("get_product_variant_key")
    product_variant_value = serializers.CharField(source='product.option_value')

    def get_product_variant_key(self, obj):
        return obj.product.option.name

    def get_final_price(self, obj):
        return obj.product.final_price

    class Meta:
        model = OrderItem
        fields = (
            'product_id', 'name', 'product_variant_id', 'product_variant_key', 'product_variant_value', 'main_image',
            'discount', 'seven_days_back', 'free_send', 'warranty',
            'quantity', 'price', 'final_price', 'sum_price', 'sum_final_price', 'sum_discount_price',)


class CartSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    count = serializers.IntegerField()
