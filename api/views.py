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
    lookup_field = 'name'

from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet


class TransactionFilter(FilterSet):
    date_gte = DateFilter(field="date", lookup_expr='gte')    
    
    class Meta:
        model = Transaction
        fields = ['date','date_gte']

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = []
    filter_class = TransactionFilter

@api_view(["GET"])
def Profit(request):
    response = get_summary()
    return Response(response)