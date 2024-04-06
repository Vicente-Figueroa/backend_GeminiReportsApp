from django.urls import path
from api_gemini.views import GeneralView, LastMonthView

urlpatterns = [
    path("general/",GeneralView.as_view()),
    path("last_month/",LastMonthView.as_view()),
]