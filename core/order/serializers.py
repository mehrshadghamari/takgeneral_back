from order.models import OrderItem
from product.models import ProductVariant
from rest_framework import serializers


class OrderlistSerializer(serializers.ModelSerializer):
    price = serializers.IntegerField()
    final_price = serializers.IntegerField()
    sum_price = serializers.IntegerField()
    sum_final_price = serializers.IntegerField()
    sum_discount_price = serializers.IntegerField()
    quantity = serializers.IntegerField()
    warranty = serializers.CharField()
    product_id = serializers.IntegerField()
    name = serializers.CharField(source="product_name")
    # main_image = productImagesSerializer(source='product_main_image', allow_null=True)
    main_image = serializers.SerializerMethodField("get_main_image")
    product_variant_id = serializers.IntegerField(source="id")
    product_variant_key = serializers.SerializerMethodField("get_product_variant_key")
    product_variant_value = serializers.CharField(source="option_value")

    def get_product_variant_key(self, obj):
        return obj.option.name

    def get_main_image(self, obj):
        request = self.context.get("request")
        img_object = obj.product_main_image
        if img_object:
            iamge_url = request.build_absolute_uri(img_object.image.url)
        else:
            iamge_url = ""
        return iamge_url

    class Meta:
        model = ProductVariant
        fields = (
            "product_id",
            "product_url",
            "name",
            "product_variant_id",
            "product_variant_key",
            "product_variant_value",
            "main_image",
            "discount",
            "free_send",
            "warranty",
            "quantity",
            "price",
            "final_price",
            "sum_price",
            "sum_final_price",
            "sum_discount_price",
        )


class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source="product.product_id")
    product_url = serializers.IntegerField(source="product.product_url")
    name = serializers.CharField(source="product.product_name")
    # main_image = productImagesSerializer(
    # source='product.product_main_image', allow_null=True)
    main_image = serializers.SerializerMethodField("get_main_image")
    discount = serializers.IntegerField(source="product.discount")
    free_send = serializers.BooleanField(source="product.free_send")
    warranty = serializers.CharField(source="product.warranty")
    price = serializers.IntegerField(source="product.price")
    final_price = serializers.SerializerMethodField()
    sum_price = serializers.IntegerField()
    sum_final_price = serializers.IntegerField()
    sum_discount_price = serializers.IntegerField()
    product_variant_id = serializers.IntegerField(source="product.id")
    product_variant_key = serializers.SerializerMethodField("get_product_variant_key")
    product_variant_value = serializers.CharField(source="product.option_value")

    def get_product_variant_key(self, obj):
        return obj.product.option.name

    def get_final_price(self, obj):
        return int(obj.product.final_price)

    def get_main_image(self, obj):
        request = self.context.get("request")
        img_object = obj.product.product_main_image
        if img_object:
            iamge_url = request.build_absolute_uri(img_object.image.url)
        else:
            iamge_url = ""
        return iamge_url

    class Meta:
        model = OrderItem
        fields = (
            "product_id",
            "product_url",
            "name",
            "product_variant_id",
            "product_variant_key",
            "product_variant_value",
            "main_image",
            "discount",
            "free_send",
            "warranty",
            "quantity",
            "price",
            "final_price",
            "sum_price",
            "sum_final_price",
            "sum_discount_price",
        )


class CartSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    count = serializers.IntegerField()


class PaymentSerializer(serializers.Serializer):
    order_id = serializers.IntegerField(required=True)
    order_description = serializers.CharField(required=False)
