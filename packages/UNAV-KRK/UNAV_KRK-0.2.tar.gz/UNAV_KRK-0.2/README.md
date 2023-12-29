# Analizador de Criptomonedas
El Analizador de Criptomonedas es una biblioteca de Python diseñada para descargar y analizar datos de criptomonedas desde la API de Kraken. Ofrece funcionalidades para visualizar la cotización de criptomonedas y calcular indicadores técnicos como el oscilador estocástico.

# Características
Descarga de datos históricos de pares de criptomonedas desde Kraken.
Cálculo del oscilador estocástico.
Generación de gráficos de velas japonesas.
Visualización de la evolución del precio y del oscilador estocástico.
# Cambios con respecto a la 0.1
Se incluye una función graficador() que contiene el código del programa princpial de tal forma que el usuario solo tenga que llamar a la función e insertar el par de monedas a graficar
# Instalación
Puede instalar el Analizador de Criptomonedas directamente desde PyPI:

### Instalar el paquete 
pip install UNAV-KRK==0.2
# Uso
A continuación, se muestra un ejemplo básico de cómo utilizar la biblioteca:

### Importar función
from src.analizador_monedas  import graficador

### Llamar a la unficón graficador()
par_moneda = "XBTEUR"

### Insertar input del par de monedas a graficar
Ingrese el par de monedas a analizar (ejemplo: XBTEUR): ETHUSDT



# Requisitos
Python 3.6 o superior.
Dependencias: krakenex, pandas, matplotlib, mplfinance. Estas se instalarán automáticamente al instalar este paquete.
# Contribuciones
Las contribuciones son bienvenidas. Si deseas contribuir, por favor:

Haz un fork del repositorio.
Crea una rama para tu característica.
Haz tus cambios y commit.
Push a tu rama y abre un pull request.
# Licencia
Este proyecto está licenciado bajo la Licencia MIT - vea el archivo LICENSE para más detalles.

