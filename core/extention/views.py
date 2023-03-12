from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from extention.models import Slider,Product,Advertisement
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
        products = Product.objects.all()
        products_serializer = ProductSerializer(products,many=True,context={"request": request})
        return Response({'sliders':slider_serializer.data,'products':products_serializer.data,},status=status.HTTP_200_OK)
    


class AdvertisementAPi(APIView):
    def get(self,request):
        advertisement = Advertisement.objects.all()
        advertisement_serializer = AdvertisementSerilizer(advertisement,many=True,context={"request": request})
        return Response(advertisement_serializer.data,status=status.HTTP_200_OK)