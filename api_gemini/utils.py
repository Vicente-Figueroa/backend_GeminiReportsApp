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

from jinja2 import Template

def call_gemini():
    genai.configure(api_key='AIzaSyBSbC28LHaIpkVg7mrNc5FI3jx6-aWCH70')

    model = genai.GenerativeModel('gemini-pro')
    ingresos, gastos = get_data()

    template = Template(open('./api_gemini/prompts/general_prompt.txt').read())

    message = template.render(gastos = gastos, ingresos = ingresos)

    response = model.generate_content(message)
    return response.text
