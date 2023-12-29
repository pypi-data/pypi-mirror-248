Analizador de Criptomonedas
El Analizador de Criptomonedas es una biblioteca de Python diseñada para descargar y analizar datos de criptomonedas desde la API de Kraken. Ofrece funcionalidades para visualizar la cotización de criptomonedas y calcular indicadores técnicos como el oscilador estocástico.

Características
Descarga de datos históricos de pares de criptomonedas desde Kraken.
Cálculo del oscilador estocástico.
Generación de gráficos de velas japonesas.
Visualización de la evolución del precio y del oscilador estocástico.
Instalación
Puede instalar el Analizador de Criptomonedas directamente desde PyPI:

bash
Copy code
pip install analizador_criptomonedas
Uso
A continuación, se muestra un ejemplo básico de cómo utilizar la biblioteca:

python
Copy code
from analizador_criptomonedas import AnalizadorMonedas

# Definir el par de monedas a analizar
par_moneda = "XBTEUR"

# Crear una instancia del analizador
analizador = AnalizadorMonedas(par_moneda)

# Ejecutar el análisis
analizador.procesar()


Requisitos
Python 3.6 o superior.
Dependencias: krakenex, pandas, matplotlib, mplfinance. Estas se instalarán automáticamente al instalar este paquete.
Contribuciones
Las contribuciones son bienvenidas. Si deseas contribuir, por favor:

Haz un fork del repositorio.
Crea una rama para tu característica.
Haz tus cambios y commit.
Push a tu rama y abre un pull request.
Licencia
Este proyecto está licenciado bajo la Licencia MIT - vea el archivo LICENSE para más detalles.

