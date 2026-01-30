# Análisis de Anuncios de Venta de Vehículos

Este proyecto consiste en una aplicación web interactiva desarrollada con **Streamlit** que permite explorar un conjunto de datos de anuncios de venta de coches en los Estados Unidos. El objetivo principal es proporcionar herramientas visuales rápidas para entender la distribución y las relaciones de las variables clave del mercado automotriz.

## Funcionalidad de la Aplicación

La aplicación web ofrece las siguientes capacidades de análisis visual:

* **Distribución del Kilometraje (Odómetro)**: A través de un histograma interactivo, el usuario puede analizar cuántas millas tienen los vehículos listados en los anuncios.
* **Relación Precio vs. Kilometraje**: Mediante un gráfico de dispersión, es posible observar cómo varía el precio de los vehículos en función de su uso (odómetro).
* **Interactividad**: El usuario puede decidir qué gráficos visualizar mediante casillas de selección (checkboxes), permitiendo una exploración personalizada de los datos.

## Tecnologías Utilizadas

* **Lenguaje**: Python
* **Librerías**:
    * `pandas`: Para la manipulación y limpieza de los datos.
    * `plotly.graph_objects`: Para la creación de gráficos interactivos y dinámicos.
    * `streamlit`: Para el desarrollo y despliegue de la interfaz de usuario web.


* `notebooks/EDA.ipynb`: Cuaderno de Jupyter con el análisis exploratorio inicial de los datos.
* `app.py`: Archivo principal que contiene la lógica de la aplicación Streamlit.
* `vehicles_us.csv`: Conjunto de datos utilizado para el análisis.
* `.streamlit/config.toml`: Configuración del servidor para el despliegue en Render.