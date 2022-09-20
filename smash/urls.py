from django.contrib import admin
from django.urls import path

from smash.views import UserObtainAuthToken, CreateTransaction, UsersList, UserTransactions

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', UserObtainAuthToken.as_view(), name='login'),
    path('transaction/', CreateTransaction.as_view(), name='transaction'),
    path('users/', UsersList.as_view(), name='user-list'),
    path('users/<str:username>/transactions', UserTransactions.as_view(), name='user-transactions'),
]
