from rest_framework.decorators import api_view
from rest_framework.response import Response
from regresion.utils import fit_model, predict_model

@api_view(["GET"])
def TrainModel(request):
    range_param = request.GET.get('range')
    response = fit_model(range_param)
    return Response(response)


@api_view(["GET"])
def PredictModel(request):
    period = request.GET.get('period')
    response = predict_model(period)
    return Response(response)