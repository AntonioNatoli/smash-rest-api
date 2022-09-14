from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from smash.authentication import CustomTokenAuthentication
from smash.models import Transaction
from smash.serializers import LoginSerializer


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
        })

class CreateTransaction(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        credits = request.data.get("credits")
        Transaction.objects.create(user=self.request.user,credits=credits)
        return Response({
            'credits': credits,
        })