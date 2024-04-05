from api_gemini.models import Transaction
from django.db.models import Sum


def get_summary():

    incomes = Transaction.objects.filter(type='Ingresos').aggregate(Sum('amount'))['amount__sum'] or 0
    expenses = Transaction.objects.filter(type='Gastos').aggregate(Sum('amount'))['amount__sum'] or 0
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