from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Product
from .serializers import HomePompDetailSerializer

class HomePompDetail(APIView):
    def get(self,request,id):
        pomp_instance=Product.objects.filter(id=id).first()
        serilizer=HomePompDetailSerializer(pomp_instance,context={"request": request})
        return Response(serilizer.data,status=status.HTTP_200_OK)