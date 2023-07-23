from order.models import Order
from order.models import OrderItem
from product.models import Product
from rest_framework import serializers


class OrderlistSerializer(serializers.ModelSerializer):
    price = serializers.IntegerField()
    final_price = serializers.IntegerField()
    sum_price = serializers.IntegerField()
    sum_final_price = serializers.IntegerField()
    sum_discount_price = serializers.IntegerField()
    quantity = serializers.IntegerField()
    warranty = serializers.CharField()
    product_id = serializers.IntegerField(source='id')

    class Meta:
        model = Product
        fields = ('product_id', 'name', 'main_image', 'discount', 'seven_days_back', 'free_send', 'warranty',
                  'quantity', 'price', 'final_price', 'sum_price', 'sum_final_price', 'sum_discount_price',)


class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.id')
    name = serializers.CharField(source='product.name')
    main_image = serializers.ImageField(
        source='product.main_image', allow_null=True)
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

    def get_final_price(self, obj):
        return obj.product.final_price

    class Meta:
        model = OrderItem
        fields = ('product_id', 'name', 'main_image', 'discount', 'seven_days_back', 'free_send', 'warranty',
                  'quantity', 'price', 'final_price', 'sum_price', 'sum_final_price', 'sum_discount_price')


class CartSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    count = serializers.IntegerField()
