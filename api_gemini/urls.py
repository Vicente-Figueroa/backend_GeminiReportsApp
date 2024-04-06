from django.urls import path
from api_gemini.views import GeneralView

urlpatterns = [
    path("general/",GeneralView.as_view()),
]