from django.urls import path
from api.views import TransactionViewSet,AccountViewSet

urlpatterns = [
    path("accounts/",AccountViewSet.as_view({'get': 'list'})),
    path("accounts/<name>/",AccountViewSet.as_view({'get': 'retrieve'})),
    path("transactions/<pk>/",TransactionViewSet.as_view({'get': 'retrieve'})),
    path("transactions/",TransactionViewSet.as_view({'get': 'list'})),
]