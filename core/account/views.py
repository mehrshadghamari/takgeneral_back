import random
from datetime import timedelta

import redis
import requests
from account.models import Address
from account.models import MyUser
from account.serializers import LogOutSerializer
from account.serializers import UserAddressSerializer
from account.serializers import UserInfoSerialozer
from account.serializers import UserRegisterOrLoginSendOTpSerializr
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView

r = redis.Redis(host="localhost", port=6379, db=0)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # Customizing JWt token claims
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["phone_number"] = user.phone_number
        # token['full_name'] = user.full_name
        # token['who'] = user.doctor_or_patient

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


def get_tokens_for_user(user):
    refresh = MyTokenObtainPairSerializer.get_token(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class GetUserInfoAndId(APIView):
    """
    helping api for front end about user info
    """

    def post(self, request):
        data = self.request.data
        access_token = data["access_token"]
        access_token_obj = AccessToken(access_token)
        user_id = access_token_obj["user_id"]
        user_full_name = access_token_obj["full_name"]
        user_phone_number = access_token_obj["phone_number"]
        return Response({"user_id": user_id, "user_full_name": user_full_name, "user_phone_number": user_phone_number})


class LogoutView(APIView):
    """
    api for logout patient
    """

    def post(self, request, *args):
        serializer = LogOutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserRegisterOrLoginSendOTp(APIView):
    """
    api for patient register
    """

    throttle_scope = "otp"

    def post(self, request):
        registered = True
        serializer = UserRegisterOrLoginSendOTpSerializr(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone_number = serializer.data["phone_number"]

            if not phone_number:
                return Response({"msg": "phone number is requierd'"}, status=status.HTTP_400_BAD_REQUEST)
            try:

                MyUser.objects.get(phone_number=phone_number)

            except MyUser.DoesNotExist:
                registered = False
                MyUser.objects.create(
                    phone_number=phone_number,
                )

            code = random.randint(10000, 99999)
            r.setex(str(phone_number), timedelta(minutes=2), value=code)
            code = r.get(str(phone_number)).decode()
            # code=cache.set(str(phone_number), code,2*60)
            # code=cache.get(str(phone_number))

            return Response(
                {"msg": "code sent successfully", "code": code, "registered": registered}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserVerifyOTP(APIView):
    """
    api for check OTp code for login patient
    """

    throttle_scope = "verfiy_code"

    def post(self, request):
        phone_number = self.request.data["phone_number"]
        code = self.request.data["code"]
        try:
            user = MyUser.objects.get(phone_number=phone_number)
        except MyUser.DoesNotExist:
            return Response({"msg": "user with this phone number does not exist"})

        # cached_code=cache.get(str(phone_number))
        cached_code = r.get(str(phone_number)).decode()
        # import pdb; pdb.set_trace()
        if code != cached_code:
            return Response({"msg": "code not matched"}, status=status.HTTP_403_FORBIDDEN)
        token = get_tokens_for_user(user)
        return Response(
            {
                "token": token,
            },
            status=status.HTTP_201_CREATED,
        )


class UserAddInfo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = MyUser.objects.get(id=request.user.id)
        serializer = UserInfoSerialozer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = MyUser.objects.get(id=request.user.id)
        serializer = UserInfoSerialozer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAdress(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_address = Address.objects.filter(user__id=request.user.id)
        serializer = UserAddressSerializer(user_address, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # user_instance =
        serializer = UserAddressSerializer(data=request.data)
        user_instance = MyUser.objects.get(id=request.user.id)
        if serializer.is_valid():
            serializer.save(user=user_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateAddress(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, id):
        address_instance = Address.objects.get(id=id)
        serializer = UserAddressSerializer(instance=address_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserStatus(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_obj = request.user
        p = str(user_obj.phone_number)
        phone_number = "0" + p[2:]
        if user_obj.full_name == " ":
            full_name = None
        else:
            full_name = user_obj.full_name
        
        if user_obj.full_name and user_obj.national_code and user_obj.phone_number :
            profile_complete = True
        else:
            profile_complete = False

        
        return Response({"phone_number": phone_number, "full_name": full_name,"profile_complete":profile_complete})


class LocationApi(APIView):
    def post(self, request):
        LATITUDE = self.request.data.get("lat", None)
        LONGITUDE = self.request.data.get("lng", None)
        TERM = self.request.data.get("term", None)
        url = f"https://api.neshan.org/v1/search?term={TERM}&lat={LATITUDE}&lng={LONGITUDE}"
        headers = {"Api-Key": "service.0378d5fd9fed448a88ea1e27a5e7f08c"}
        req = requests.get(url=url, headers=headers)
        return Response(req.json(), status=req.status_code)
