import datetime
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from smash.authentication import CustomTokenAuthentication
from smash.models import Transaction
from smash.permissions import StaffPermission
from smash.serializers import LoginSerializer, UserSerializer, TransactionSerializer
from django.contrib.auth.models import User

from smash.utils import get_none_or_value


class UserObtainAuthToken(APIView):
    permission_classes = (~IsAuthenticated,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'is_staff': user.is_staff
        })


class CreateTransaction(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        credits = request.data.get("credits")
        Transaction.objects.create(user=self.request.user, credits=credits)
        return Response({
            'credits': credits,
        })


class UserTransactions(APIView, LimitOffsetPagination):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated, StaffPermission]

    # def get(self, request):
    #
    #     month = get_none_or_value(self.request.GET.get('month'))
    #     year = self.request.GET.get('year')
    #
    #     user = User.objects.get(username=username)
    #     transaction_list = Transaction.objects.filter(user=user)
    #
    #     if year:
    #         transaction_list = transaction_list.filter(purchase_date__year=year)
    #
    #     if month:
    #         transaction_list = transaction_list.filter(purchase_date__month=month)
    #
    #     # return transaction_list.order_by('-purchase_date')
    def get(self, request, username, format=None):

        month = get_none_or_value(self.request.GET.get('month'))
        year = self.request.GET.get('year')

        user = User.objects.get(username=username)
        transaction_list = Transaction.objects.filter(user=user)

        if year:
            transaction_list = transaction_list.filter(purchase_date__year=year)

        if month:
            transaction_list = transaction_list.filter(purchase_date__month=month)

        count = transaction_list.count()
        total_credits = transaction_list.aggregate(total_credits=Coalesce(Sum('credits'), 0.0))['total_credits']
        results = self.paginate_queryset(transaction_list.order_by('-purchase_date'), request, view=self)
        serializer = TransactionSerializer(results, many=True)

        return JsonResponse({
            "results": serializer.data,
            "count": count,
            "total_credits": round(total_credits, 2)
        })
        # return self.get_paginated_response(serializer.data)


class UsersList(ListAPIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated, StaffPermission]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(is_staff=False)




