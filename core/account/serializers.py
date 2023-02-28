from django.core import validators
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, TokenError

from account.models import MyUser


class UserRegisterOrLoginSendOTpSerializr(serializers.Serializer):
    phone_number=serializers.CharField(validators=[
                                              validators.RegexValidator(r'^989[0-3,9]\d{8}$',
                                                                        ('Enter a valid mobile number.'), 'invalid')])
        
        

class LogOutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': ('Token is invalid or expired')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
