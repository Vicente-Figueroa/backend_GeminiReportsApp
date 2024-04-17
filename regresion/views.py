from rest_framework.decorators import api_view
from rest_framework.response import Response
from regresion.utils import fit_model, predict_model

@api_view(["GET"])
def TrainModel(request):
    response = fit_model()
    return Response(response)


@api_view(["GET"])
def PredictModel(request):
    response = predict_model()
    return Response(response)