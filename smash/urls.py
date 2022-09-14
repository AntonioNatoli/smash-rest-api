from django.contrib import admin
from django.urls import path

from smash.views import UserObtainAuthToken, CreateTransaction

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', UserObtainAuthToken.as_view(), name='login'),
    path('transaction/', CreateTransaction.as_view(), name='transaction'),
]
