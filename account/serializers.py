from account.models import Address
from account.models import MyUser
from django.core import validators
from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import TokenError


class UserRegisterOrLoginSendOTpSerializr(serializers.Serializer):
    phone_number = serializers.CharField(validators=[
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


class UserInfoSerialozer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name',
                  'phone_number', 'email', 'national_code',)
        read_only_fields = ('phone_number',)


    def validate_national_code(self, value):
        """
        Validate that the national_code is unique.
        """
        if MyUser.objects.filter(national_code=value).exists():
            raise serializers.ValidationError("This national code is already in use vvv.")
        return value


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        # fields='__all__'
        fields = ('id','title', 'post_code', 'full_address',
                  'pelak', 'vahed', 'lt', 'lng')
