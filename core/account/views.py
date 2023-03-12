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
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework.throttling import ScopedRateThrottle


from account.serializers import LogOutSerializer,UserRegisterOrLoginSendOTpSerializr,UserInfoSerialozer,UserAddressSerializer

from account.models import MyUser,Address

r = redis.Redis(host='localhost', port=6379, db=0)


# def get_id(token):
#     token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
#     data = {'token': token}
#     try:
#       valid_data = TokenBackend(algorithm='HS256').decode(token,verify=True)
#       user = valid_data['user']
#     except :
#         pass
#     return


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # Customizing JWt token claims
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['phone_number'] = user.phone_number
        # token['full_name'] = user.full_name
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
    throttle_scope = 'otp'

    def post(self, request):
        registered=True
        serializer=UserRegisterOrLoginSendOTpSerializr(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone_number=serializer.data['phone_number']
        
            if not phone_number:
                return Response({"msg": "phone number is requierd'"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                
                MyUser.objects.get(phone_number=phone_number)

            except MyUser.DoesNotExist:
                registered=False
                MyUser.objects.create(
                    phone_number=phone_number,)

            code = random.randint(10000, 99999)
            code=cache.set(str(phone_number), code,2*60)
            code=cache.get(str(phone_number))

            return Response({"msg": "code sent successfully","code":code,"registered":registered}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserVerifyOTP(APIView):
    """
    api for check OTp code for login patient
    """
    throttle_scope = 'verfiy_code'

    def post(self, request):
        phone_number = self.request.data['phone_number']
        code = self.request.data['code']
        try:
            user = MyUser.objects.get(phone_number=phone_number)
        except MyUser.DoesNotExist:
            return Response({'msg':'user with this phone number does not exist'})

        cached_code=cache.get(str(phone_number))
        
        if str(code) != str(cached_code):
            return Response({"msg": "code not matched"}, status=status.HTTP_403_FORBIDDEN)
        token = get_tokens_for_user(user)
        return Response({"token":token,}, status=status.HTTP_201_CREATED)




class UserAddInfo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = MyUser.objects.get(id=request.user.id)
        serializer = UserInfoSerialozer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request):
        user= MyUser.objects.get(id=request.user.id)
        serializer=UserInfoSerialozer(instance=user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserAddAdress(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user_address = Address.objects.filter(user__id = request.user.id)        
        serializer = UserAddressSerializer(user_address)
        return Response(serializer.data,status = status.HTTP_200_OK)

    def post(self,request):
        # user_instance = 
        serializer = UserAddressSerializer(data=request.data)
        user_instance=MyUser.objects.get(id=request.user.id)
        if serializer.is_valid():
            serializer.save(user = user_instance)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    

class UserStatus(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        print('***************************')
        print(type(request.user.phone_number))
        p=str(request.user.phone_number)
        print(p[2:])
        phone_number='0'+p[2:]
        return Response({'phone_numer':phone_number,'full_name':request.user.full_name})