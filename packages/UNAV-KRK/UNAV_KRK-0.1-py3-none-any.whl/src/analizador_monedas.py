import krakenex
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf



class AnalizadorMonedas:
    def __init__(self, par_moneda):
        self.par_moneda = par_moneda
        self.datos = None

    def descargar_datos(self):
        k = krakenex.API()
        # Solicitar datos semanales estableciendo el intervalo en 10080 (minutos en una semana)
        response = k.query_public('OHLC', {'pair': self.par_moneda, 'interval': 10080})
        if response['error']:
            raise ValueError(f"Error al descargar datos para {self.par_moneda}: {response['error']}")
        self.datos = pd.DataFrame(response['result'][self.par_moneda], columns=['time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count'])
        self.datos['time'] = pd.to_datetime(self.datos['time'], unit='s')
        for col in ['open', 'high', 'low', 'close', 'vwap', 'volume']:
            self.datos[col] = self.datos[col].astype(float)
    def calcular_estocastico(self, k_period=14, d_period=3):
        df = self.datos
        df['low_k'] = df['low'].rolling(window=k_period).min()
        df['high_k'] = df['high'].rolling(window=k_period).max()
        df['%K'] = (df['close'] - df['low_k']) / (df['high_k'] - df['low_k']) * 100
        df['%D'] = df['%K'].rolling(window=d_period).mean()

    def graficar_cotizaciones(self):
        # Asegurarse de que los datos estocásticos estén calculados
        if '%K' not in self.datos.columns or '%D' not in self.datos.columns:
            self.calcular_estocastico()

        # Crear el gráfico de velas japonesas
        apds = [mpf.make_addplot(self.datos['%K'], panel=1, color='blue', ylabel='%K'),
                mpf.make_addplot(self.datos['%D'], panel=1, color='orange', ylabel='%D')]

        # Establecer el estilo de las velas
        mpf_style = mpf.make_marketcolors(up='green', down='red', edge='inherit', wick='inherit', volume='in',
                                          inherit=True)
        s = mpf.make_mpf_style(base_mpf_style='classic', marketcolors=mpf_style)

        # Configurar y mostrar el gráfico de velas con el oscilador estocástico
        fig, axes = mpf.plot(self.datos.set_index('time'),
                             type='candle',
                             style=s,
                             addplot=apds,
                             title=f'Cotizaciones y Oscilador Estocástico para {self.par_moneda}',
                             ylabel='Cotización',
                             volume=False,
                             figsize=(10, 8),
                             panel_ratios=(6, 3),  # Ajustar las proporciones de los paneles
                             returnfig=True)

        # Personalizar y mostrar el gráfico
       # axes[0].legend(['Cotización'])
        axes[2].legend(['%K', '%D'])
        plt.show()

    def graficar_estocastico(self):
        df = self.datos
        plt.figure(figsize=(10, 6))
        plt.subplot(2, 1, 1)
        plt.plot(df['time'], df['close'])
        plt.title(f'Estocástico y Cotizaciones para {self.par_moneda}')
        plt.ylabel('Cotización')

        plt.subplot(2, 1, 2)
        plt.plot(df['time'], df['%K'], label='%K')
        plt.plot(df['time'], df['%D'], label='%D')
        plt.ylabel('Estocástico')
        plt.legend()
        #plt.show()

    # Método para ejecutar todo el proceso
    def procesar(self):
        try:
            self.descargar_datos()
            self.calcular_estocastico()
            self.graficar_cotizaciones()
            self.graficar_estocastico()
        except Exception as e:
            print(f"Error durante el procesamiento: {e}")

# Función para obtener y mostrar la lista de pares de monedas disponibles
def obtener_pares_disponibles():
    k = krakenex.API()
    response = k.query_public('AssetPairs')
    pares_disponibles = list(response['result'].keys())
    return pares_disponibles

#cambio de prue