from rest_framework import viewsets
from api_gemini.models import Account, Transaction
from api.serializers import AccountSerializer, TransactionSerializer
from django_filters.rest_framework import DateFilter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.utils import get_summary, get_categories
from django.db.models import Sum 
 
class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = []

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = []
    filterset_fields = ['account__name', 'type']

@api_view(["GET"])
def Profit(request):
    response = get_summary()
    return Response(response)

@api_view(["GET"])
def CategoryView(request):
    response =get_categories(request)
    return Response(response)