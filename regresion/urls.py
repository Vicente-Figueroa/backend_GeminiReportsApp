from django.urls import path
from regresion.views import TrainModel, PredictModel

urlpatterns = [
    path("train_model/",TrainModel),
    path("predict/",PredictModel),
]