from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from extention.models import Slider,Products,Advertisement
from extention.serializers import SliderSerializer,ProductSerializer,AdvertisementSerilizer




class SliderApi(APIView):
    def get(self,request):
        slider=Slider.objects.all()
        slider_serializer=SliderSerializer(slider,many=True,context={"request": request})
        # return Response(serializer.data,status=status.HTTP_200_OK)



class HomeApi(APIView):
    def get(self,request):
        slider = Slider.objects.all()
        slider_serializer = SliderSerializer(slider,many=True,context={"request": request})
        products = Products.objects.all()
        products_serializer = ProductSerializer(products,many=True,context={"request": request})
        advertisement = Advertisement.objects.all()
        advertisement_serializer = AdvertisementSerilizer(advertisement,many=True,context={"request": request})
        return Response({'sliders':slider_serializer.data,'products':products_serializer.data,'advertisements':advertisement_serializer.data},status=status.HTTP_200_OK)