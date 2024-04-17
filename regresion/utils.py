from api_gemini.models import Transaction
from django.db.models import Sum
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pickle
from datetime import date

def convertir_a_dataframe(modelo):
    # Obtiene los objetos del modelo

    # Obtiene la fecha actual
    fecha_actual = date.today()
    objetos = modelo.objects.filter(date__year=2024)

    # Crea una lista vacía para almacenar los datos
    datos = []

    # Recorre cada objeto del modelo
    for objeto in objetos:
        # Crea un diccionario con los atributos del objeto
        dato = {
            # Agrega los atributos que deseas incluir en el DataFrame
            'date': objeto.date,
            'amount': objeto.amount,
            'type': objeto.type,
            'cuenta': objeto.account,
        }

        # Agrega el diccionario a la lista
        datos.append(dato)

    # Crea un DataFrame de Pandas a partir de la lista de datos
    df = pd.DataFrame(datos)

    # Devuelve el DataFrame
    return df


def transformar_data():
    transacciones = convertir_a_dataframe(Transaction)

    # Transforma fecha a formato DateTime y extrae solo la fecha
    transacciones['date'] = pd.to_datetime(transacciones['date']).dt.date

    # Filtra solo transacciones de tipo "Gastos"
    transacciones_filtradas = transacciones[transacciones['type'] == 'Gastos']

    # Cálculo de z-scores y detección de outliers
    zscores = np.abs(transacciones_filtradas['amount'] - transacciones_filtradas['amount'].mean()) / transacciones_filtradas['amount'].std()
    transacciones_filtradas = transacciones_filtradas[zscores <= 3]  # Umbral de 3 desviaciones estándar

    # Ordena por fecha y calcula monto acumulado
    transacciones_filtradas = transacciones_filtradas.sort_values(by='date')
    transacciones_filtradas['amount_acumulado'] = transacciones_filtradas['amount'].cumsum()

    # Agrupa por día, calcula sumas y acumula sumas
    transacciones_por_dia = transacciones_filtradas.groupby('date')
    transacciones_por_dia_acumulado = pd.DataFrame()
    transacciones_por_dia_acumulado['amount'] = transacciones_por_dia['amount'].sum()
    transacciones_por_dia_acumulado['sum_amount'] = transacciones_por_dia_acumulado['amount'].cumsum()

    # Elimina la primera fila (sin fecha anterior)
    transacciones_por_dia_acumulado = transacciones_por_dia_acumulado.iloc[1:]

    # Convierte la fecha a formato numérico y agrega a la columna 'date_num'
    serie = pd.to_datetime(transacciones_por_dia_acumulado.reset_index().date)
    serie = pd.to_numeric(serie).values
    transacciones_por_dia_acumulado['date_num'] = serie

    return transacciones_por_dia_acumulado



def fit_model():
    transacciones_por_dia_acumulado = transformar_data()
    # Convertir la fecha a formato adecuado para la regresiónfrom sklearn.model_selection import train_test_split
    X = transacciones_por_dia_acumulado[['date_num']]
    y = transacciones_por_dia_acumulado['sum_amount']
    # Crea una instancia de MinMaxScaler y aplícala a las variables x e y
    scaler_X = MinMaxScaler()
    scaler_y = MinMaxScaler()
    X_scaled = scaler_X.fit_transform(X)
    y_scaled = scaler_y.fit_transform(y.values.reshape(-1, 1))  # Convertir y en matriz 2D
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    with open('regresion/modelos/modelo_entrenado.pkl', 'wb') as f:
        pickle.dump(model, f)
    # Guarda el scaler de X con pickle
    with open('regresion/modelos/scaler_x.pkl', 'wb') as f:
        pickle.dump(scaler_X, f)

    # Guarda el scaler de Y con pickle
    with open('regresion/modelos/scaler_y.pkl', 'wb') as f:
        pickle.dump(scaler_y, f)

    return {
        "response" : "OK",
        "Error cuadrático medio (MSE)" : mse,
        "Coeficiente de determinación (R²):" : r2
    }

def predict_model():
    # Definición de datos originales
    data = {"fecha": pd.to_datetime(["17/04/2024", "18/04/2024", "19/04/2024"], format="%d/%m/%Y")}
    fechas_originales = pd.DataFrame(data)

    # Generar fechas ampliadas (10 días antes y después)
    fecha_min = fechas_originales["fecha"].min() - pd.DateOffset(days=10)
    fecha_max = fechas_originales["fecha"].max() + pd.DateOffset(days=20)

    rango_fechas = pd.date_range(start=fecha_min, end=fecha_max, freq='D')

    # Expandir el DataFrame original
    data_ampliada = {"fecha": rango_fechas}
    fechas_extendidas = pd.DataFrame(data_ampliada)
    # Carga el scaler de X con pickle
    with open('regresion/modelos/scaler_x.pkl', 'rb') as f:
        scaler_x_cargado = pickle.load(f)

    # Carga el scaler de Y con pickle
    with open('regresion/modelos/scaler_y.pkl', 'rb') as f:
        scaler_y_cargado = pickle.load(f)
    # Carga el modelo entrenado con pickle
    with open('regresion/modelos/modelo_entrenado.pkl', 'rb') as f:
        modelo_cargado = pickle.load(f)

    fechas_futuras = pd.DataFrame(fechas_extendidas)  # Ajustar fechas# Preparar datos de fechas para predicciones
    fechas_futuras_scaled = scaler_x_cargado.transform(fechas_futuras['fecha'].values.reshape(-1, 1))

    # Realizar predicciones
    predicciones_escaladas = modelo_cargado.predict(fechas_futuras_scaled)

    # Invertir la escala de las predicciones
    predicciones = scaler_y_cargado.inverse_transform(predicciones_escaladas.reshape(-1, 1))

    # Mostrar o guardar las predicciones
    fechas_extendidas["predicciones"] = predicciones
    # prompt: Quiero que mi df fechas_extendidas ahora sea un dict con un formato bonito

    fechas_extendidas["fecha"] = fechas_extendidas["fecha"].dt.strftime('%d/%m/%Y')

    diccionario_predicciones = {}

    for i in range(len(fechas_extendidas)):
        diccionario_predicciones[fechas_extendidas["fecha"][i]] = fechas_extendidas["predicciones"][i]

    return {"estado": "Ok",
            "records": diccionario_predicciones}