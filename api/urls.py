from django.urls import path
from api.views import AccountListView

urlpatterns = [
    path("accounts/",AccountListView.as_view()),
]