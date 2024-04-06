from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import call_gemini 

class GeneralView(APIView):
    """
    Esta vista simple recibe un mensaje y devuelve otro.
    """
    @classmethod
    def get_extra_actions(cls):
        return []

    def get(self, request):
        # Obtenemos el mensaje de la solicitud
        #message = request.data['message']
        response_call = call_gemini()
        # Generamos la respuesta
        response = {
            'message': response_call,
        }

        # Devolvemos la respuesta
        return Response(response)