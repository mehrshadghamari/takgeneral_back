import random
import redis
from datetime import timedelta
import jdatetime
import requests
import json

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.cache import cache
from django.shortcuts import render
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from account.serializers import LogOutSerializer

from account.models import MyUser

r = redis.Redis(host='localhost', port=6379, db=0)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # Customizing JWt token claims
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['phone_number'] = user.phone_number
        token['full_name'] = user.full_name
        # token['who'] = user.doctor_or_patient

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


def get_tokens_for_user(user):
    refresh = MyTokenObtainPairSerializer.get_token(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class GetUserInfoAndId(APIView):
    """
     helping api for front end about user info
    """

    def post(self, request):
        data = self.request.data
        access_token = data['access_token']
        access_token_obj = AccessToken(access_token)
        user_id = access_token_obj['user_id']
        user_full_name = access_token_obj['full_name']
        user_phone_number = access_token_obj['phone_number']
        # who = access_token_obj['who']
        return Response({'user_id': user_id, 'user_full_name': user_full_name,'user_phone_number': user_phone_number})




class LogoutView(APIView):
    """
    api for logout patient
    """
    def post(self, request, *args):
        serializer = LogOutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserRegisterOrLoginSendOTp (APIView):
    """
    api for patient register
    """

    def post(self, request):
        register=False
        phone_number = self.request.data['phone_number']
        if not phone_number:
            return Response({"msg": "phone number is requierd'"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            
            MyUser.objects.get(phone_number=phone_number)

        except MyUser.DoesNotExist:
            register=True
            MyUser.objects.create(
                phone_number=phone_number, is_active=False,)
            
        print('**************************************')
        print(type(phone_number))
        code = random.randint(10000, 99999)
        # code = r.setex(str(phone_number), timedelta(minutes=2), value=code)
        code=cache.set(str(phone_number), code,2*60)
        # register=cache.set(str(phone_number), register,)
        # code = r.setex(str(phone_number)+'0', timedelta(minutes=2), value=register)
        print('*****************************')
        # code=r.get(str(phone_number)).decode()
        code=cache.get(str(phone_number))
        print(code)

        return Response({"msg": "code sent successfully","code":code,}, status=status.HTTP_200_OK)


class UserVerifyOTP(APIView):
    """
    api for check OTp code for login patient
    """

    def post(self, request):
        phone_number = self.request.data['phone_number']
        patient = MyUser.objects.get(phone_number=phone_number)
        code = self.request.data['code']
        # cached_code = r.get(str(phone_number)).decode()
        cached_code=cache.get(str(phone_number))
        # register = cache.get(str(phone_number))
        if str(code) != str(cached_code):
            return Response({"msg": "code not matched"}, status=status.HTTP_403_FORBIDDEN)
        token = get_tokens_for_user(patient)
        return Response({"token":token,}, status=status.HTTP_201_CREATED)

