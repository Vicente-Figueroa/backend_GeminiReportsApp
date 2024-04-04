from django.contrib.auth.models import User
from rest_framework import generics
from api_gemini.models import Account
from api.serializers import AccountSerializer

class AccountListView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer