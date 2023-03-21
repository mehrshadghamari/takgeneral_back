from django.shortcuts import render
from django.db.models import F,Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from extention.models import Slider,ProductClassification,Advertisement
from product.models import Product
from extention.serializers import SliderSerializer,ProductClassificationSerializer,AdvertisementSerilizer
from product.serializers import AllProductSerializer



class SliderApi(APIView):
    def get(self,request):
        slider=Slider.objects.all()
        slider_serializer=SliderSerializer(slider,many=True,context={"request": request})
        # return Response(serializer.data,status=status.HTTP_200_OK)



class HomeApi(APIView):
    def get(self,request):
        slider = Slider.objects.all()
        slider_serializer = SliderSerializer(slider,many=True,context={"request": request})
        products = ProductClassification.objects.all()
        products_serializer = ProductClassificationSerializer(products,many=True,context={"request": request})
        special_offer_products=Product.objects.filter(special_offer=True)
        special_offer_serializer=AllProductSerializer(special_offer_products,many=True,context={"request": request})
        amazing_offer_product=Product.objects.filter(discount__gte=20)
        # amazing_offer_product=Product.objects.with_final_price().annotate(ekhtelaf=F('price') - F('final_price')).filter(ekhtelaf__gte=1000000)
        # amazing_offer_product=Product.objects.annotate(final_price=F('price')-(F('price')*F('discount')/100)).annotate(ekhtelaf=F('price') - F('final_price')).filter(ekhtelaf__gte=1000000)
        # amazing_offer_product=Product.objects.annotate(ekhtelaf=F('price') - F('final_price')).filter(ekhtelaf__gte=1000000)
        amazing_offer_serializer=AllProductSerializer(amazing_offer_product,many=True,context={"request": request})
        return Response({'sliders':slider_serializer.data,'products':products_serializer.data,'special_offer_products':special_offer_serializer.data,'amazing_offer_product':amazing_offer_serializer.data},status=status.HTTP_200_OK)
    


class AdvertisementAPi(APIView):
    def get(self,request):
        advertisement = Advertisement.objects.all()
        advertisement_serializer = AdvertisementSerilizer(advertisement,many=True,context={"request": request})
        return Response(advertisement_serializer.data,status=status.HTTP_200_OK)