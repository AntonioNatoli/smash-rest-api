from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from smash.api_errors import UserNotExist, PasswordWrong


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(
        write_only=True
    )

    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not User.objects.filter(username__iexact=email).exists() and not User.objects.filter(
                email__iexact=email).exists():
            raise UserNotExist()
        elif User.objects.filter(username__iexact=email).exists():
            email = User.objects.get(username__iexact=email).username
        elif User.objects.filter(email__iexact=email).exists():
            email = User.objects.get(email__iexact=email).email

        user = authenticate(request=self.context.get('request'),
                            username=email, password=password)

        if not user:
            raise PasswordWrong()

        attrs['user'] = user

        return attrs
