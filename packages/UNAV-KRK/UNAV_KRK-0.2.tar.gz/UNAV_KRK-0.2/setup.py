from setuptools import setup, find_packages

setup(
    name='UNAV_KRK',
    version='0.2',
    packages=find_packages(),
    description='Descarga y plotea monedas de kraken',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='A.Tapia',
    author_email='altapia7@gmail.com',
    url='https://github.com/TapiaR/AnaliMon/tree/master',
    install_requires=[
        'krakenex',
        'pandas',
        'matplotlib',
        'mplfinance'
        # otras dependencias
    ],
    python_requires='>=3.6',
    # Puedes agregar más metadatos como clasificadores
)
