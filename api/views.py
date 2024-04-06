from rest_framework import viewsets
from api_gemini.models import Account, Transaction
from api.serializers import AccountSerializer, TransactionSerializer
from django_filters.rest_framework import DateFilter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.utils import get_summary

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = []

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = []
    filterset_fields = ['account__name']

@api_view(["GET"])
def Profit(request):
    response = get_summary()
    return Response(response)