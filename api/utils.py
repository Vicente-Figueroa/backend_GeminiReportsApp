from api_gemini.models import Transaction
from django.db.models import Sum
# Import the date and timedelta classes from the datetime module
from datetime import date, timedelta
from api_gemini.choices import envelopedIdChoices as envelopeIdChoices

# Get the current date and convert it to ISO 8601 format
current_date = date.today().isoformat()

# Calculate the date 30 days before the current date and convert it to ISO 8601 format
days_before = (date.today() - timedelta(days=30)).isoformat()


def get_summary():

    incomes = Transaction.objects.filter(type='Ingresos',date__gte=days_before).aggregate(Sum('amount'))['amount__sum'] or 0
    expenses = Transaction.objects.filter(type='Gastos',date__gte=days_before).aggregate(Sum('amount'))['amount__sum'] or 0
    profit = incomes + expenses
    ratio = ( expenses / incomes ) * -1
    ratio_desc = 'positive'

    # si el gasto es mayor al ingreso
    if ratio > 1:
        ratio = ratio -1
        ratio_desc = 'negative'
    
    # armar la salida
    output_dict = {
        'incomes': incomes,
        'expenses': expenses,
        'profit':profit,
        'ratio': float('{0:.2f}'.format(ratio)),
        'ratio_desc' : ratio_desc,
    }
    return output_dict

def get_categories(request):
     # Si no hay parámetro 'envelope_id' en la solicitud, devolver todas las categorías y sus totales
    if 'envelope_id' not in request.query_params:
        # Obtener todas las categorías únicas
        envelope_id_choices = dict(envelopeIdChoices).values()

        # Calcular el total de cada categoría
        response_data = []
        for envelope_id_choice in envelope_id_choices:
            envelope_id = next((k for k, v in envelopeIdChoices if v == envelope_id_choice), None)
            if envelope_id is not None:
                total = Transaction.objects.filter(envelope_id=envelope_id,date__gte=days_before).aggregate(total_amount=Sum('amount'))['total_amount'] or 0
                if total is not 0:
                    response_data.append({'envelope_id': envelope_id_choice, 'total': total})

        return response_data

    # Obtener la variable 'envelope_id' de la solicitud
    envelope_id_choice = request.query_params.get('envelope_id')

    # Encontrar el valor numérico del 'envelope_id' correspondiente al choice
    envelope_id = next((k for k, v in envelopeIdChoices if v == envelope_id_choice), None)
    if envelope_id is None:
        return {'error': 'Invalid envelope_id choice'}

    # Filtrar las transacciones por el envelope_id
    transacciones = Transaction.objects.filter(envelope_id=envelope_id,date__gte=days_before)

    # Calcular el total del campo 'amount'
    total = transacciones.aggregate(total_amount=Sum('amount'))['total_amount']
    response_data ={
        'envelope_id': envelope_id_choice,
        'total': total
    }
    return response_data