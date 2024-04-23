import google.generativeai as genai
import pandas as pd
from mistune import Markdown
from bs4 import BeautifulSoup
from api_gemini.models import Transaction
from jinja2 import Template
from django.db.models import Sum
# Import the date and timedelta classes from the datetime module
from datetime import date, timedelta

# Get the current date and convert it to ISO 8601 format
current_date = date.today().isoformat()

# Calculate the date 30 days before the current date and convert it to ISO 8601 format
days_before = (date.today() - timedelta(days=30)).isoformat()


def get_data(period):
    if period == 'todo':
        transacciones_ingresos = Transaction.objects.filter(type='Ingresos')
        transacciones_gastos = Transaction.objects.filter(type='Gastos')
        ingresos = transacciones_ingresos.aggregate(total_ingresos=Sum('amount'))['total_ingresos']
        gastos = transacciones_gastos.aggregate(total_gastos=Sum('amount'))['total_gastos']
        return ingresos, gastos
    
    if period == 'ultimo_mes':
        transacciones_ingresos = Transaction.objects.filter(
            type='Ingresos',
            date__gte=days_before
            )
        transacciones_gastos = Transaction.objects.filter(type='Gastos',date__gte=days_before)
        ingresos = transacciones_ingresos.aggregate(total_ingresos=Sum('amount'))['total_ingresos']
        gastos = transacciones_gastos.aggregate(total_gastos=Sum('amount'))['total_gastos']
        return ingresos, gastos


def call_gemini(period):
    genai.configure(api_key='AIzaSyAtQwglcD0LvJdhKcbb2KCNjHhiSAepvqQ')
    model = genai.GenerativeModel('gemini-pro')
    # get data
    ingresos, gastos = get_data(period)

    template = Template(open('./api_gemini/prompts/general_prompt.txt').read())
    message = template.render(gastos = gastos, ingresos = ingresos, periodo=period)

    response = model.generate_content(message)
    return response.text
