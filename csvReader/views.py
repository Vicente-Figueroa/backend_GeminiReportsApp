from rest_framework.views import APIView
from rest_framework.response import Response
from api_gemini.models import Account, Transaction
import pandas as pd

class ImportCSVView(APIView):
    @classmethod
    def get_extra_actions(cls):
        return []

    def post(self, request, *arg, **kwargs):
        csv_file = request.FILES['csv_file']

        data = pd.read_csv(csv_file, delimiter=';')
        
        # sacar el account name para las variables
        account_names = data['account'].unique().tolist()

        for name in account_names:
            to_insert = {'name':name}
            object_model = Account.objects.get_or_create(**to_insert)

        # Sacar la transaccion
        datos_modelo = data.to_dict(orient="records")

        for datos in datos_modelo:
            # Obtener el objeto Account o crearlo si no existe.
            cuenta, _ = Account.objects.get_or_create(name=datos["account"])

            # Crear un nuevo objeto en el modelo.
            modelo = Transaction(
                account=cuenta,
                amount=datos["amount"],
                type=datos["type"],
            )

            # Guardar el objeto del modelo.
            modelo.save()
        response = {'estado' : 'OK'}
        return Response(response)
                