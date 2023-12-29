import unittest
from unittest.mock import patch, MagicMock
from src.analizador_monedas import AnalizadorMonedas
import pandas as pd
import os

class TestAnalizadorMonedas(unittest.TestCase):

    def setUp(self):
        # Ruta al archivo CSV en la carpeta data
        self.datos_prueba_csv = os.path.join(os.path.dirname(__file__), 'data', 'XZCEUR.csv')
        self.analizador = AnalizadorMonedas("XZCEUR")

    def cargar_datos_prueba(self):
        # Cargar los datos de prueba desde el archivo CSV
        return pd.read_csv(self.datos_prueba_csv)

    @patch('src.analizador_monedas.krakenex.API')
    def test_descargar_datos(self, mock_krakenex):
        # Cargar datos de prueba desde el CSV
        datos_prueba = self.cargar_datos_prueba()

        # Crear un objeto MagicMock para simular la respuesta de la API
        mock_response = MagicMock()
        mock_response.return_value = {
            'error': [],
            'result': {
                'XZCEUR': datos_prueba.values.tolist()  # Convertir los datos del DataFrame a una lista de listas
            }
        }
        mock_krakenex.return_value.query_public = mock_response

        # Ejecutar el método descargar_datos que debería utilizar los datos simulados
        self.analizador.descargar_datos()

        # Verificaciones para asegurar que los datos se han cargado correctamente
        self.assertIsNotNone(self.analizador.datos)
        self.assertIn('time', self.analizador.datos.columns)
        self.assertEqual(len(self.analizador.datos), len(datos_prueba))


if __name__ == '__main__':
    unittest.main()


