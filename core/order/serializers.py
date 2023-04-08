from rest_framework import serializers
from product.models import Product




class OrderlistSerializer(serializers.ModelSerializer):
    price=serializers.IntegerField()
    final_price= serializers.IntegerField()
    sum_price=serializers.IntegerField()
    sum_final_price=serializers.IntegerField()
    sum_discount_price=serializers.IntegerField()
    quantity = serializers.IntegerField()
    warranty=serializers.CharField()

    class Meta:
        model=Product
        fields=('id','name','main_image','discount','seven_days_back','free_send','warranty','quantity','price','final_price','sum_price','sum_final_price','sum_discount_price',)




class CartSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    count=serializers.IntegerField()


# class ParentOrderInput(serializers.Serializer):
    # datas=serializers.ListField(child=ChildOrderInput(many=True))