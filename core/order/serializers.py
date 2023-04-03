from rest_framework import serializers
from product.models import Product




class OrderlistSerializer(serializers.ModelSerializer):
    sum_price=serializers.FloatField()
    sum_final_price=serializers.FloatField()
    sum_discount_price=serializers.FloatField()
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