from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from extention.models import Slider
from extention.serializers import SliderSerializer




class SliderApi(APIView):
    def get(self,request):
        slider=Slider.objects.all()
        serializer=SliderSerializer(slider,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
