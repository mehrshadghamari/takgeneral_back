from django.shortcuts import render
from django.db.models import F,Value,FloatField
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from product.models import Product
from .serializers import OrderlistSerializer



class ShoworderlistBeforLogin(APIView):
    def post(self,request):
        datas = self.request.data['cartsData']
        # datas=[{'id':3,'count':3},{'id':2,'count':1}]
        l=[]
        all_count=0
        for data in datas:
            all_count+=data['count']
            p=Product.objects.with_final_price().filter(id=data['id']).annotate(quantity=Value(data['count'],FloatField()),sum_price = F('final_price_Manager') * Value(data['count'],FloatField()))
            l.append(p.first())

            
        
        serz=OrderlistSerializer(l,many=True)

        return Response({'order_list':serz.data,'all_count':all_count},status=status.HTTP_200_OK)


