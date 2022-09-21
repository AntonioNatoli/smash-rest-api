from django.contrib import admin
from django.urls import path

from smash.views import UserObtainAuthToken, CreateTransaction, UsersList, UserTransactions, InvoiceCredits, UserDetail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', UserObtainAuthToken.as_view(), name='login'),
    path('transaction/', CreateTransaction.as_view(), name='transaction'),
    path('invoice-credits/', InvoiceCredits.as_view(), name='invoice-credits'),
    path('users/', UsersList.as_view(), name='user-list'),
    path('users/<str:username>/transactions', UserTransactions.as_view(), name='user-transactions'),
    path('users/<str:username>/statement', UserDetail.as_view(), name='user-statement'),
]
