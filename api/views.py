from django.contrib.auth.models import User
from rest_framework import generics, viewsets
from api_gemini.models import Account, Transaction
from api.serializers import AccountSerializer, TransactionSerializer

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = []
    lookup_field = 'name'


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = []
