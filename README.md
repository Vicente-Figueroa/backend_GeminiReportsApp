Descripción del proyecto: Backend para app de finanzas con IA
Este repositorio presenta un backend para una aplicación que integra el modelo de inteligencia artificial Gemini para analizar datos financieros. La aplicación toma como entrada un archivo CSV de una app de gastos y utiliza Gemini para generar un reporte personalizado con información y análisis relevantes.

Motivación:

El objetivo del proyecto es explorar la integración de grandes modelos de lenguaje (LLM) como Gemini en aplicaciones cotidianas. La app permite a los usuarios:

Obtener una vista completa de sus finanzas: Visualizar sus gastos e ingresos de forma organizada y comprensible.
Identificar patrones de consumo: Descubrir tendencias en sus hábitos de gasto y áreas donde puede optimizar su presupuesto.
Recibir recomendaciones personalizadas: Obtener consejos y sugerencias basadas en sus datos financieros y objetivos personales.
Funcionalidades:

Importación de datos: Carga un archivo CSV desde una app de gestión financiera.
Análisis con IA: Utiliza Gemini para procesar y analizar los datos financieros.
Generación de reportes: Crea un reporte personalizado con información y análisis relevantes.
Tecnologías:

Backend: Python, Django, DjangoRest
Modelo de IA: Gemini
Base de datos: PostgreSQL
Guía de inicio rápido:

Instalar dependencias: pip install -r requirements.txt
Configurar base de datos: Editar archivo settings.py con información de la base de datos.
Ejecutar servidor: python manage.py runserver
Importar datos: Cargar archivo CSV desde la interfaz web.
Generar reporte: Acceder a la sección "Reportes" para obtener un análisis personalizado