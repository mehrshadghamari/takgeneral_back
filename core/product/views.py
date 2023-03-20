from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Product
from .serializers import HomePompDetailSerializer,ProductIDSerializer

class HomePompDetail(APIView):
    def get(self,request,id):
        pomp_instance=Product.objects.filter(id=id).first()
        serilizer=HomePompDetailSerializer(pomp_instance,context={"request": request})
        return Response(serilizer.data,status=status.HTTP_200_OK)
    


class ProductID(APIView):
    def get(self,request,id):
        ids=Product.objects.all().values_list('id')[:30]
        srz=ProductIDSerializer(ids)
        return Response(srz.data,status=status.HTTP_200_OK)