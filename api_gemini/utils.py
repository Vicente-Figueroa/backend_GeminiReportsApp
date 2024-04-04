import google.generativeai as genai
import pandas as pd
from mistune import Markdown
from bs4 import BeautifulSoup
from api_gemini.models import Transaction

from django.db.models import Sum

def get_data():

    transacciones_ingresos = Transaction.objects.filter(type='Ingresos')
    transacciones_gastos = Transaction.objects.filter(type='Gastos')

    ingresos = transacciones_ingresos.aggregate(total_ingresos=Sum('amount'))['total_ingresos']
    gastos = transacciones_gastos.aggregate(total_gastos=Sum('amount'))['total_gastos']
    return ingresos, gastos


def call_gemini():
    genai.configure(api_key='AIzaSyBSbC28LHaIpkVg7mrNc5FI3jx6-aWCH70')

    model = genai.GenerativeModel('gemini-pro')
    ingresos, gastos = get_data()
    message = f"""Hola gemini, este es una prueba de concepto.
     Quiero que analices mis ingresos en el año que son estos =  {ingresos}
     y tambien mis gastos en el año que son estos{gastos}. Dime que tal mi situacion financiera actual"""


    response = model.generate_content(message)
    return response.text
