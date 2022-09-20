import datetime

from django.db.models import Sum
from django.db.models.functions import Coalesce
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from smash.api_errors import UserNotExist, PasswordWrong
from smash.models import Transaction


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


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['credits', 'purchase_date', 'username']


class UserSerializer(serializers.ModelSerializer):
    total_credits = serializers.SerializerMethodField()
    total_credits_current_month = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'total_credits', 'total_credits_current_month']

    def get_total_credits(self, obj):
        transaction_list = Transaction.objects.filter(user=obj)
        return round(transaction_list.aggregate(total_credits=Coalesce(Sum('credits'), 0.0))['total_credits'] ,2)

    def get_total_credits_current_month(self, obj):
        transaction_list = Transaction.objects.filter(user=obj, purchase_date__month=datetime.datetime.now().month)
        return round(transaction_list.aggregate(total_credits=Coalesce(Sum('credits'), 0.0))['total_credits'] ,2)



