from django.urls import path
from regresion.views import TrainModel, PredictModel

urlpatterns = [
    path("profit/",TrainModel),
    path("PredictModel/",PredictModel),
]