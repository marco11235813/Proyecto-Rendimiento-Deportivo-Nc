import zipfile
import numpy as np
import pandas as pd
import os
import missingno as msno
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
from collections import Counter
import re


import warnings
warnings.filterwarnings(action= 'ignore')




def Imagen(path_relativo: str, size: tuple[int,int], path_absoluto:  None|str= None):

    """
    Esta funcion recibe un path relativo referente a una imagen (o un path absoluto), y el tamaño/dimensiones que
    debe tener en forma de tupla (width, height)

    devuelve la imagen pasada con las dimensiones obtenidas

    parameters: path_relativo (str), size (tuple[int,int]), path_absoluto(None,str)

    returns: None
    """

    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg



    # Load image
    image = mpimg.imread(path_relativo)
    # Let the axes disappear
    plt.figure(figsize= size)
    plt.axis('off')
    # Plot image in the output
    image_plot = plt.imshow(image)



# Abre e instancia los ficheros (comprimidos en formato .zip o que esten en .csv)
def instanciar_data(path: str) -> str|pd.DataFrame:

    """
    Instancia un DataFrame a partir de un archivo CSV, ya sea directamente o desde un archivo ZIP.
    
    Args:
        path (str): La ruta del archivo CSV o ZIP que contiene el CSV.
        
    Returns:
        pd.DataFrame: El DataFrame instanciado a partir del archivo CSV.
        str: Mensaje de error si la ruta o el archivo no existen.
    """

    # Verificar si la ruta o el archivo existe
    if os.path.exists(path):
        # Evaluar si es un archivo .zip
        if path.lower().endswith('.zip'):
            # Instanciar el archivo comprimido en un objeto ZipFile
            with zipfile.ZipFile(path, 'r') as f:
                # Listar los archivos contenidos en el .zip
                file = f.namelist()
                if not file:
                    return 'El archivo .zip está vacío'
                
                # Abrir el archivo .csv que contiene
                with f.open(file[0], 'r') as p:
                    # Instanciar el .csv en un objeto DataFrame
                    df = pd.read_csv(p)
        else:
            # Leer el archivo .csv directamente
            with open(path, 'r', encoding='utf-8') as p:
                df = pd.read_csv(p)
        return df
    else:
        return 'El archivo o la ruta del archivo no existe'


#- INFORME PRELIMINAR

#- VERIFICAR EL TIPO DE DATOS.

def verificar_tipo_datos(df):

    '''
    Realiza un análisis de los tipos de datos y la presencia de valores nulos en un DataFrame.

    Esta función toma un DataFrame como entrada y devuelve un resumen que incluye información sobre
    los tipos de datos en cada columna, el porcentaje de valores no nulos y nulos, así como la
    cantidad de valores nulos por columna.

    Parameters:
        df (pandas.DataFrame): El DataFrame que se va a analizar.

    Returns:
        pandas.DataFrame: Un DataFrame que contiene el resumen de cada columna, incluyendo:
        - 'nombre_campo': Nombre de cada columna.
        - 'tipo_datos': Tipos de datos únicos presentes en cada columna.
        - 'no_nulos_%': Porcentaje de valores no nulos en cada columna.
        - 'nulos_%': Porcentaje de valores nulos en cada columna.
        - 'nulos': Cantidad de valores nulos en cada columna.
    '''

    mi_dict = {"nombre_campo": [], "tipo_datos": [], "no_nulos_%": [], "nulos_%": [], "nulos": []}

    for columna in df.columns:
        porcentaje_no_nulos = (df[columna].count() / len(df)) * 100
        mi_dict["nombre_campo"].append(columna)
        mi_dict["tipo_datos"].append(df[columna].apply(type).unique())
        mi_dict["no_nulos_%"].append(round(porcentaje_no_nulos, 2))
        mi_dict["nulos_%"].append(round(100-porcentaje_no_nulos, 2))
        mi_dict["nulos"].append(df[columna].isnull().sum())

    df_info = pd.DataFrame(mi_dict)

    return df_info



#- INFORME DEL DATA FRAME.

def informe_dataframe(dataframe: pd.DataFrame) -> None:

    """
    esta funcion obtiene un dataframe, y realiza un informe analizando y explorando algunas caracteristicas del
    dataframe centrandose principalmente en caracteristicas a nivel general de nuestro dataframe y realizando un procesamiento de
    algunos datos obteniendo metricas e informacion

    devuelve un informe que contiene:

    -Dimensiones del DataFrame
    -Numero de datos
    -Filas y Columnas
    -Tipo de columnas
    -Cantidad de registros duplicados
    -Metricas Generales

    Parameters: data (pandas.DataFrame).

    Returns: None.

    """

    df = dataframe

    print('INFORME PRELIMINAR SOBRE CARACTERISTICAS DEL DATASET:\n')
    print(f'--Dimensiones del DataFrame--\nFilas: {df.shape[0]}\nColumnas: {df.shape[1]}\n')
    print(f'--Numero de datos--\n{df[df.isna() == False].count().sum()}\n')
    print(f'--Filas y Columnas--\nFilas: muestra de indices-------> {list(df.index)[0:5]}  -----> Desde {list(df.index)[0]}  Hasta {list(df.index)[-1]}\nColumnas: {list(df.columns)}\n')
    print(f'--Tipo de columnas--\n{df.dtypes}')
    columnas= df.columns

    if 'hours' in columnas and 'attributes' not in columnas:
        print(f'--Cantidad de registros duplicados--\n{df.drop(columns=["hours"]).duplicated().sum()}\n')
    elif 'hours' not in columnas and 'attributes' in columnas:
        print(f'--Cantidad de registros duplicados--\n{df.drop(columns=["attributes"]).duplicated().sum()}\n')
    elif 'hours' in columnas and 'attributes' in columnas:
        print(f'--Cantidad de registros duplicados--\n{df.drop(columns=["hours","attributes"]).duplicated().sum()}\n')
    else:
        print(f'--Cantidad de registros duplicados--\n{df.duplicated().sum()}\n')


    # print(f'--Estadisticos preliminares generales--\n{df.describe()}\n')

    return ('~'*50)+'oo'+('~'*50)



#----------------------------------------------------------------------------------------------------

#- INFORME DE COLUMNA.

def informe_columna(df: None|pd.DataFrame, columna: None|str) -> None:

    """
    esta funcion obtiene un dataframe y el nombre de una de sus columnas, y realiza un informe analizando y explorando algunas caracteristicas de
    la feature, centrandose principalmente en caracteristicas a nivel general y realizando un procesamiento de 
    algunos datos obteniendo metricas e informacion

    Dependiendo el tipo de dato contenido en la feature/columna, devolvera informacion ligeramente diferente:

    Para tipo object:

    -Numero de datos nulos
    -Cantidad de valores unicos en la columna
    -Valores unicos en la columna (Primeros 5 valores, en caso de exceder los 5, en caso contrario, devuelve todos los valores unicos)
    -Moda de la columna
    -Distribucion de frecuencias

    Para tipo datetime64[ns]:

    -Numero de datos nulos
    -Cantidad de valores unicos en la columna
    -Valores unicos en la columna (una muestra de 4 valores como ejemplo, y el rango que abarcan (desde que valor hasta que valor))
    -Moda de la columna
    -Distribucion de frecuencias
    -Valor maximo y minimo

    Para tipo numerico (int, float):

    -Numero de datos nulos
    -Valores unicos en la columna (una muestra de 5 valores como ejemplo, y el rango que abarcan (desde que valor hasta que valor))
    -Moda de la columna
    -Estadisticos Principales de la columna
    -Valores extremos
    -Distribucion de frecuencias
    -Valor maximo y minimo


    Parameters: data (pandas.DataFrame), columna (str).

    Returns: None.
    
    """

    data = df[columna]
    
    # print(f'Informe preliminar sobre la columna/feature {columna}:\n')
    print(f'INFORME PRELIMINAR SOBRE LA COLUMNA/FEATURE {columna}:\n')
    if data.dtype == 'object' or data.dtype == 'bool':
        print(f'--Numero de datos nulos--\n{data.isna().sum()}\n')
        print(f'--Cantidad de valores unicos en la columna--\n{data.describe()[1]}\n')

        if len(data.unique()) > 5:
            print(f'--Valores unicos en la columna (Primeros 5 valores)--\n{data.unique()[0:5]}\n')
        else:
            print(f'--Valores unicos en la columna--\n{data.unique()}\n')
            
        print(f'--Moda de la columna especificada--\nValor modal -----> {data.describe()[2]}\nFrecuencia acumulada ------> {data.describe()[3]}\n')
        print(f'--Distribucion de frecuencias (primeros valores con mayor cantidad de frecuencias)--\n {data.value_counts().nlargest(3)}\n')
        print('-'*120)
        print('-'*120)
    elif data.dtype == 'datetime64[ns]':
        print(f'--Numero de datos nulos--\n{data.isna().sum()}\n')
        print(f'--Cantidad de valores unicos en la columna--\n{data.describe()[1]}\n')
        ## En el print siguinte, realizamos un formateo de los valores de la columna, ya que la salida predeterminada (el output) agrega otros valores que hacen la intrepretacion mas dificil e incomoda
        print(f'--Valores unicos en la columna--\nEj: {data.dt.strftime("%Y-%m-%d").unique()[0:3]}  -----> Desde {list(data.dt.strftime("%Y-%m-%d").unique())[0]}  Hasta {list(data.dt.strftime("%Y-%m-%d").unique())[-1]}\n')
        print(f'--Moda de la columna especificada--\nValor modal -----> {data.describe()[2]}\nFrecuencia acumulada ------> {data.describe()[3]}\n')
        print(f'--Distribucion de frecuencias (primeros valores con mayor cantidad de frecuencias)--\n {data.value_counts().nlargest(3)}\n')
        print(f'--Valor maximo y minimo--\nMaximo: {data.max()}\nMinimo: {data.min()}\n')
        print('-'*120)
        print('-'*120)
    else:
        print(f'--Numero de datos nulos--\n{data.isna().sum()}\n')
        print(f'--Valores unicos en la columna--\nEj: {data.unique()[0:5]}  -----> Desde {list(data.unique())[0]}  Hasta {list(data.unique())[-1]}\n')
        print(f'--Estadisticos Principales de la columna--\nMedia: {round(data.mean(),2)}\nDesviacion Estandar: {round(data.std(),2)}\nPrimer cuartil: {data.quantile(0.25)}\nMediana: {data.median()}\nTercer cuartil: {data.quantile(0.75)}\n')
        print(f'--Valores extremos--\nValor maximo: {data.max()}\nValor minimo: {data.min()}\n')
        print(f'--Distribucion de frecuencias (primeros valores con mayor cantidad de frecuencias)--\n {data.value_counts().nlargest(3)}\n')
        print(f'--Valor maximo y minimo--\nMaximo: {data.max()}\nMinimo: {data.min()}\n')
        print('-'*120)
        print('-'*120)
    return


#----------------------------------------------------------------------------------------------------



#- VISUALIZACIÓN DE NULOS.

# Subplot

def visualizar_nulos(df: pd.DataFrame|None) -> None:

    """
    Toma como parametro un dataframe pandas y realiza la construccion de 4 graficos principales en
    base al analisis de sus datos con valor np.nan o nulos:

    Matrix Plot: Una cuadrícula donde cada fila representa una observación y cada columna representa una variable en el DataFrame.
    Los valores nulos están marcados en blanco en la cuadrícula.

    Bar Plot: Un gráfico de barras vertical que muestra la cantidad de valores nulos en cada columna del DataFrame.
    Cada barra vertical representa una columna, y la altura de la barra indica la cantidad de valores nulos en esa columna.

    Heatmap: Similar a la matriz, pero con colores para resaltar las áreas con más valores nulos.
    Los valores nulos pueden estar representados con colores más oscuros para destacar las áreas con más ausencias de datos.

    Dendrogram: Un diagrama de árbol que agrupa las variables y observaciones basadas en la similitud de los patrones de valores nulos.
    Las ramas del árbol se fusionan según la similitud de los patrones de valores nulos entre las variables y observaciones.

    Parameters: df (pandas.DataFrame)

    returns: None

    """

    fig, axes = plt.subplots(1, 2, figsize=(15, 10))

    msno.matrix(df, ax=axes[0])
    msno.bar(df, ax=axes[1])  


    axes[0].set_title('Matrix Plot')
    axes[1].set_title('Bar Plot')


    plt.tight_layout()
    plt.show()


    fig, axes = plt.subplots(1, 2, figsize=(15, 10))
    msno.heatmap(df, ax=axes[0])
    msno.dendrogram(df, ax=axes[1])


    axes[0].set_title('Heatmap')
    axes[1].set_title('Dendrogram')

    plt.tight_layout()
    plt.show()




#----------------------------------------------------------------------------------------------------



#- VALORES ATÍPICOS, EXTREMOS Y OUTLIERS.



# Columnas Cualitativas.

import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re

def analisis_frecuencia_palabras(dataframe: pd.DataFrame):
    """
    Toma como parámetro un dataframe pandas, selecciona las columnas tipo 'object', 
    realiza una serie de normalización y procesamiento de los datos, y genera un gráfico 
    de barras por cada columna seleccionada que representa las palabras más frecuentes en la columna.

    parameters: dataframe (pandas.DataFrame)

    returns: None
    """
    if dataframe is None:
        raise ValueError("El DataFrame proporcionado es None.")
        
    # Seleccionar columnas de tipo 'object'
    columnas_cualitativas = dataframe.select_dtypes(include=['object']).columns.tolist()

    for columna in columnas_cualitativas:
        # Asegurarse de que todos los valores son de tipo str y manejar valores nulos
        dataframe[columna] = dataframe[columna].astype(str).fillna('')

    for columna in columnas_cualitativas:
        # Procesamiento de texto
        texto_columna = dataframe[columna].str.lower().str.replace(r'[^a-zA-Z\s]', '', regex=True).str.split()
        palabras_columna = [word for sublist in texto_columna for word in sublist]
        frecuencia_palabras = Counter(palabras_columna)
        palabras_mas_frecuentes = frecuencia_palabras.most_common(10)
        
        # Separar palabras y sus frecuencias
        if palabras_mas_frecuentes:
            palabras, frecuencias = zip(*palabras_mas_frecuentes)
        else:
            palabras, frecuencias = [], []
        
        # Generar gráfico de barras
        plt.figure(figsize=(10, 6))
        plt.bar(palabras, frecuencias)
        plt.xticks(rotation=90)
        plt.xlabel('Palabra')
        plt.ylabel('Frecuencia')
        plt.title(f'Palabras más frecuentes en la columna {columna}')
        plt.show()

# Ejemplo de uso
# df = pd.read_csv('tu_archivo.csv')
# analisis_frecuencia_palabras(df)


#----------------------------------------------------------------------------------------------------


def boxplots_numericas(dataframe: pd.DataFrame|None) -> None:

    """
    Toma como parametro un pandas.DataFrame y devuelve un boxplot de
    cada columna de tipo numerico (varibles cuantitativas)

    parameters: dataframe (pd.DataFrame|None)

    returns: None
    """
    if dataframe is None:
        raise ValueError("El DataFrame proporcionado es None.")
    df_numericas = dataframe.select_dtypes(include=['number'])
    for columna in df_numericas.columns:
        sns.boxplot(x=dataframe[columna])
        plt.title(f'Diagrama de caja para {columna}')
        plt.show()

#----------------------------------------------------------------------------------------------------


# - VALORES DUPLICADOS.

def hist_duplicados(dataframe: str|pd.DataFrame) -> None:

    """
    Esta funcion toma como parametro un pandas.DataFrame.
    
    Da salida a un grafico de barras/histograma que refleja la cantidad de registros duplicados y no duplicados
    presentes en el dataframe

    En el Caso que no se registren duplicados, dara salida a un mensaje confirmandolo

    parameters: dataframe(str|pandas.DataFrame)

    returns: None
    """

    columnas= dataframe.columns

    if 'hours' in columnas and 'attributes' not in columnas:
        df_duplicates= dataframe.drop(columns=["hours"]).duplicated().value_counts()
    elif 'hours' not in columnas and 'attributes' in columnas:
        df_duplicates= dataframe.drop(columns=["attributes"]).duplicated().value_counts()
    elif 'hours' in columnas and 'attributes' in columnas:
        df_duplicates= dataframe.drop(columns=["hours","attributes"]).duplicated().value_counts()
    else:
        df_duplicates= dataframe.duplicated().value_counts()
        
    df_duplicates = pd.DataFrame({'Duplicados': df_duplicates.index, 'Frecuencia': df_duplicates.values})
    if not df_duplicates.empty: 
        sns.barplot(x='Duplicados', y='Frecuencia', data=df_duplicates)
        plt.title('Conteo de Frecuencias de Registros Duplicados')
        plt.xlabel('Duplicados')
        plt.ylabel('Frecuencia')
        plt.xticks([0, 1], ['No Duplicados', 'Duplicados'])
        plt.show()
    else:
        print("No se encontraron registros duplicados.")



#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------




#- PARA ANÁLISIS DESCRIPTIVO

#----------------------------------------------------------------------------------------------------

def descripcion_distribucion(df: pd.DataFrame):
    '''
    Crea una serie de gráficos de barras y de torta que muestran la distribución de los valores de la feature/columna.

    También imprime una serie de valores y métricas básicas en referencia a los valores y distribución de valores de la columna/feature

    Parameters:
        df (pandas.DataFrame): El DataFrame que contiene los datos de la recopilación de features de ICFES.

    Returns:
        None
    '''

    columnas = df.columns

    for columna in columnas:
        muestra = df[columna].value_counts().nlargest(10)

        plt.figure(figsize=(20, 10))

        if df[columna].dtype == 'object' or df[columna].dtype == 'datetime64[ns]':
            # Gráfico de barras
            plt.subplot(1, 2, 1)
            ax = sns.barplot(x=muestra.index, y=muestra.values, data=muestra.to_frame().reset_index())
            ax.set_title(f'Gráfico de distribución de frecuencias (primeros 5 valores) {columna}')
            ax.set_xlabel(columna)
            ax.set_ylabel('Cantidad de frecuencias')
            plt.xticks(rotation=45)

            # Gráfico de torta para las proporciones representativas de los datos
            plt.subplot(1, 2, 2)
            try:
                plt.pie(x=muestra, labels=muestra.index, shadow=True, autopct='%1.1f%%')
            except ValueError:
                muestra = muestra[:5]  # Tomar solo las 5 categorías principales
                plt.pie(x=muestra, labels=muestra.index, shadow=True, autopct='%1.1f%%')
            plt.title('Distribución Relativa de Valores')
            plt.xlabel(columna)
            plt.xticks(rotation=45)
            plt.grid()
        else:
            # Diagrama de caja para columnas numéricas
            plt.subplot(1, 2, 1)
            sns.boxplot(x=df[columna])
            plt.title(f'Diagrama de caja para {columna}')

            # Gráfico de torta para las proporciones representativas de los datos
            plt.subplot(1, 2, 2)
            try:
                plt.pie(x=muestra, labels=muestra.index, shadow=True, autopct='%1.1f%%')
            except ValueError:
                muestra = muestra[:5]  # Tomar solo las 5 categorías principales
                plt.pie(x=muestra, labels=muestra.index, shadow=True, autopct='%1.1f%%')
            plt.title('Distribución Relativa de Valores')
            plt.xlabel(columna)
            plt.xticks(rotation=45)
            plt.grid()


        # Mostrar el gráfico
        plt.show()

        # Mostrar algunas estadísticas básicas
        print('\n')
        print('Estadísticas Básicas')
        print('\n')
        print(df[columna].describe())
        print('-' * 160)
        print('-' * 160)
        print('\n')

#----------------------------------------------------------------------------------------------------
## APPEARANCES
def apariciones_x_jugador(df):

    """Esta funcion obtiene un dataframe y trabaja con la columna player_id,
    devuelve un grafico de barras que muestra la frecuencia acumulada de las
     apariciones de jugadores en partidos.

     Parameters: df (DataFrame)

     Returns: Barplot
    
    """
    # cambiamos el tipo de dato de la columna player_id
    df['player_id'] = df['player_id'].astype(str)

    # agrupamos la data en cuanto a frecuencias acumuladas, ordenamos de manera descendente segun la cantidad de frecuencias
    data = df['player_id'].value_counts().nlargest(5).reset_index().sort_values(by= 'player_id', ascending= False)

    #graficamos
    plt.figure(figsize= (16,8))
    sns.barplot(data= data, x='index', y='player_id', palette= 'viridis')

    # Agregar el etiqueta con valor exacto en cada bin
    for index, value in enumerate(data['player_id']):
        plt.text(index, value, str(value), ha='center', va='bottom')

    plt.xlabel('Jugador')
    plt.ylabel('Cantidad de apariciones')
    plt.xticks(rotation= 45)
    plt.title('Cantidad de apariciones por jugador\n(primeros 5 con mayor cantidad)')
    plt.show()
    

    jugadores = {}
    ids = list(data['index'].unique())
    # ids = ['38253','32467','59561','65230','74229']
    for llave in ids:
        jugadores.setdefault(llave, str(list(df['player_name'][df['player_id'] == llave].unique())[0]))
    return jugadores

#----------------------------------------------------------------------------------------------------


def minutos_x_partido(df):

    """Esta funcion toma un Dataframe y trabaja con su columna minutes_played.
    Devuelve una serie de graficos que muestran la distribucion y dispersion de valores de minutos jugados
    por jugador por partido

    Parameteers: df (DataFrame)

    Returns: Boxplot, Pie, Barplot
    
    """
    data = df['minutes_played'].value_counts().nlargest(7).reset_index().sort_values(by= 'minutes_played', ascending= False)
    # print(data['minutes_played'])
    # 1-Boxplot
    plt.figure(figsize= (16,8))
    plt.subplot(1,2,1)
    sns.boxplot(data= df, x= df['minutes_played'].astype(int))
    plt.title('Distribucion de minutos jugados (por jugador por partido)')
    plt.xlabel('Minutos Jugados')

    
    # 2-Pie
    plt.subplot(1,2,2)
    plt.pie(x= data['minutes_played'],  shadow= True,  autopct='%1.1f%%')
    plt.title('Proporción de Minutos Jugados\n(por jugador por partido)')
    plt.legend('Minutos Jugados', data['index'])
    plt.xlabel('Minutos Jugados')

    plt.show()

    data['index'] = data['index'].astype(str)

    # 3-Barras o Histograma
    plt.figure(figsize= (16,8))
    sns.barplot(data= data, x= data['index'], y= data['minutes_played'])
    plt.title('Minutos jugados por jugadores en cada partido')
    plt.xlabel('Minutos_jugados')
    plt.ylabel('Cantidad de jugadores')

    # Agregar el etiqueta con valor exacto en cada bin
    for index, value in enumerate(data['minutes_played']):
        plt.text(index, value, str(value), ha='center', va='bottom')


    plt.show()


#----------------------------------------------------------------------------------------------------

def tarjetas_x_jugador(df):

    """Esta funcion toma un dataframe y realiza una agrupacion de datos de cantidades de tarjetas por jugador

    Devuelve un grafico de barras con los 10 jugadores con mayor cantidad de tarjetas.

    Parameters: df (DataFrame).

    Returns: barplot. 
    
    """
    data = df.groupby('player_id').agg({'yellow_cards': 'sum', 'red_cards': 'sum'}).reset_index()
    data['total_cards'] = data['yellow_cards'] + data['red_cards']
    data = data.nlargest(10, 'total_cards').sort_values(by= 'total_cards', ascending= False)
    
    # Calcula la posición base de las barras rojas
    base_position = data['red_cards'].values

    #graficamos
    plt.figure(figsize= (16,8))

    # Obtener las alturas de las barras amarillas y rojas
    yellow_heights = data['yellow_cards'].values
    red_heights = data['red_cards'].values

    # Coordenadas de x para las barras
    x = np.arange(len(data))

    # Graficar las barras amarillas
    plt.bar(x, yellow_heights, color='yellow', label='Tarjetas Amarillas')

    # Graficar las barras rojas, apiladas sobre las amarillas
    plt.bar(x, red_heights, bottom=yellow_heights, color='red', label='Tarjetas Rojas')



    plt.title('Cantidad de tarjetas por jugador')
    plt.xlabel('Jugador')
    plt.ylabel('Cantidad de tarjetas')
    plt.xticks(x, data['player_id'])
    plt.show()

    return data
#----------------------------------------------------------------------------------------------------


def goles_y_asistencias(df):

    """ Esta función agrupa el DataFrame por 'player_id' y el año de la columna 'date',
    sumando los goles y asistencias para cada jugador en cada año.
    Luego, genera gráficos de barras para cada año mostrando la participación total en goles de cada jugador.

    Parameters: df (DataFrame)

    Returns: barplots
    """
    df['year']= df['date'].dt.year
    data = df.groupby(['player_id', 'player_name', 'year']).agg({'goals': 'sum', 'assists': 'sum'}).reset_index()
    data['total_participacion_goles'] = data['goals'] + data['assists']

    por_temporada = data.sort_values(by= ['year', 'total_participacion_goles'], ascending= [True, False])
    años = df['date'].dt.year.unique()

    # Se define el número de filas y columnas para la cuadrícula de subgráficos
    n_filas = 7
    n_columnas = 2

    # Se crea una figura con subgráficos en una cuadrícula de 2*7
    fig, axes = plt.subplots(n_filas, n_columnas, figsize=(20, 30))

    # Se itera a través de los años y crea un gráfico por año
    for i, año in enumerate(años):
        fila = i // n_columnas
        columna = i % n_columnas
        
        # temp = (por_temporada[por_temporada['year'] == año]
        #         .groupby('player_id')['total_participacion_goles'])

        temp = por_temporada[por_temporada['year'] == año].set_index('player_id')['total_participacion_goles'].nlargest(5)
        
        # Se configura el subgráfico actual
        ax = axes[fila, columna]
        temp.plot(ax=ax, kind='bar')
        ax.set_title('Año ' + str(año)) ; ax.set_xlabel('Jugador') ; ax.set_ylabel('Goles + Asistencias')
        ax.legend_ = None
    
    plt.tight_layout()
    plt.show()

    return por_temporada
#----------------------------------------------------------------------------------------------------
##CLUBS

def tamaño_promedio_plantillas(df):

    """Esta función calcula el tamaño promedio de las plantillas de los clubes
    y genera un gráfico de barras con los 7 clubes con el tamaño promedio más grande,
    junto con una línea que muestra el promedio general del tamaño de las plantillas.
    
    Parameters: df (DataFrame)

    Returns: Dataframe, barplot
    """
    # agrupamos los datos por club_id y por nombre (para obtener las etiquetas)

    df = df[df['squad_size'] > 0] # filtramos los valores 0, ya que originalmente no contenian dato en el campo squad_size y producirian sesgo en el valor promedio
    data = df.groupby(['club_id', 'name']).agg({'squad_size': 'mean'}).sort_values(by= 'squad_size', ascending= False).reset_index()
    muestra= data.nlargest(7, columns= 'squad_size') # tomamos solamente los 7 valores con mayor promedio
    promedio_general = data['squad_size'].mean()

    #graficamos
    plt.figure(figsize= (16,8))

    sns.barplot(data= muestra, x= 'name', y= 'squad_size', color= 'green')

   # Agregamos una línea roja que muestra el promedio general del tamaño de las plantillas
    plt.axhline(y=promedio_general, color='red', linestyle='--', label= f'Valor promedio: {promedio_general: .2f}')

    plt.title('Distribucion de promedios de tamaño de plantillas (primeros 7 clubes)')
    plt.xlabel('Club')
    plt.ylabel('Promedio cantidad integrantes')
    plt.xticks(rotation= 45)
    plt.legend(loc= 'upper right')

    plt.tight_layout() # ajustamos el grafico
    plt.show()

    return data

#----------------------------------------------------------------------------------------------------


def extranjeros_x_club(df):

    """ Visualiza la distribución de la cantidad de jugadores extranjeros por club 
    para los 10 clubes con más jugadores extranjeros.

    Parameters: df (Dataframe)

    Returns: DataFrame, barplot.
    
    """
    data = df.groupby(['club_id', 'name']).agg({'foreigners_number': 'sum'}).sort_values(by= 'foreigners_number', ascending= False).reset_index()
    data = data.nlargest(10, columns= 'foreigners_number')

    plt.figure(figsize= (16,8))

    sns.barplot(data= data, x= 'name', y= 'foreigners_number', color= 'brown')

    plt.title('Distribucion cantidad de jugadores extranjeros por club (primeros 10)')
    plt.xlabel('Club')
    plt.ylabel('Cantidad de jugadores')
    plt.xticks(rotation= 45)
    
    plt.show()


    return data

#----------------------------------------------------------------------------------------------------


def jugadores_en_selecciones(df):

    """ Visualiza la distribución de la cantidad de jugadores en selecciones nacionales
    por club para los 10 clubes con más jugadores en selecciones.

    Parameters: df (Dataframe)

    Returns: DataFrame, barplot.
    
    """
    data = df.groupby(['club_id', 'name']).agg({'national_team_players': 'sum'}).sort_values(by= 'national_team_players', ascending= False).reset_index()
    data = data.nlargest(10, columns= 'national_team_players')

    plt.figure(figsize= (16,8))

    sns.barplot(data= data, x= 'name', y= 'national_team_players', color= 'black')

    plt.title('Distribucion cantidad de jugadores en selecciones nacionales\npor club (primeros 10)')
    plt.xlabel('Club')
    plt.ylabel('Cantidad de jugadores en selecciones')
    plt.xticks(rotation= 45)
    
    plt.show()


    return data



#----------------------------------------------------------------------------------------------------


def estadio_x_tamaño_club(df):

    """Esta función analiza la relación entre la capacidad del estadio y el tamaño del club.
    
    Parámetros: df (DataFrame): DataFrame que contiene los datos del club, incluyendo 
                las columnas 'club_id', 'name', 'stadium_seats' y 'squad_size'.
    
    Retorna: DataFrame (DataFrame ordenado por 'stadium_seats' y 'squad_size').
    
    """

    data = df[['club_id', 'name', 'stadium_seats', 'squad_size']].sort_values(by= ['stadium_seats', 'squad_size'], ascending= [False, False])
    corr= data[['stadium_seats', 'squad_size']].corr()
    print(f'\nValor de Correlacioin lineal entre la capacidad del estadio y el tamaño del club:\n')
    print(corr)

    # graficamos
    plt.figure(figsize= (16,8))
    sns.scatterplot(data= data, x= 'squad_size', y= 'stadium_seats')

    plt.title('Relacion Capacidad del estadio vs Tamaño del Club')
    plt.xlabel('Tamaño del Club')
    plt.ylabel('stadium_seats')

    plt.show()


    return data
#----------------------------------------------------------------------------------------------------

def transferencias_x_club(df):

    """Esta función analiza las transferencias netas por club y grafica los 10 primeros clubes
    con mayores valores netos de transferencia.

    Parámetros: df (DataFrame): DataFrame que contiene los datos del club, incluyendo 
                las columnas 'name' y 'net_transfer_record'.

    Retorna: DataFrame (DataFrame con los 10 clubes con mayores valores netos de transferencia).
    
    
    """
    temp = df[df['net_transfer_record'] > 0.0]
    data = temp[['name', 'net_transfer_record']].sort_values(by= 'net_transfer_record', ascending= False).nlargest(10, columns= 'net_transfer_record')
    data_mean= temp['net_transfer_record'].mean()

    plt.figure(figsize= (16,8))
    sns.barplot(data= data, x= 'name', y= 'net_transfer_record')

    plt.axhline(y= data_mean , color= 'red', linestyle= '--', label= f'Promedio de clubes: {round(data_mean, 2)}' )

    plt.title('Transferencias Netas por club (10 primeros)')
    plt.xlabel('Club')
    plt.ylabel('Valor neto (en miles de euros)')
    plt.xticks(rotation= 45)
    plt.legend(loc= 'upper right')

    plt.show()


    return data

#----------------------------------------------------------------------------------------------------
##CLUB_GAMES

def goles_x_local_o_oponente(df):

    """ Esta función analiza y grafica la distribución de los marcadores de goles propios y del oponente
    en partidos, mostrando los 7 marcadores más frecuentes y sus proporciones.

    Parámetros: df (DataFrame): DataFrame que contiene los datos de los partidos, incluyendo 
                las columnas 'game_id', 'own_goals' y 'opponent_goals'.

    Retorna: DataFrame (DataFrame con los 7 marcadores más frecuentes y sus frecuencias).
    
    """

    temp = df[['game_id', 'own_goals', 'opponent_goals']]
    data = temp.groupby(['game_id']).agg({'own_goals': 'first', 'opponent_goals': 'first'}).reset_index()
    data['scores'] = data['own_goals'].astype(str) + '-' + data['opponent_goals'].astype(str)
    muestra = data['scores'].value_counts().reset_index().nlargest(7, columns= 'scores')


    # graficamos
    plt.figure(figsize= (20,10))

    plt.subplot(1,2,1)
    sns.barplot(data= muestra, x= muestra['index'], y= muestra['scores'])
    plt.title('Distribucion de marcador en partidos (entre los 7 mas frecuentes)')
    plt.xlabel('Marcador(own -- opponent)')
    plt.ylabel('Frecuencia')
    plt.xticks(rotation= 45)

    plt.subplot(1,2,2)
    plt.pie(data= muestra, x= muestra['scores'], labels= muestra['index'], shadow= True, autopct= '%1.1f%%')
    plt.title('Proporcion de Marcadores (entre los 7 primeros)')
    plt.xlabel('Marcadores')

    plt.tight_layout()
    plt.show()


    plt.figure(figsize= (20,10))
    # Gráfico de distribución de goles propios vs goles del opone
    plt.subplot(1,2,1)
    sns.histplot(data=data, x='own_goals', y='opponent_goals', bins=30, pthresh=0.1, cmap="Blues")
    plt.title('Distribución de goles propios vs goles del oponente')
    plt.xlabel('Goles propios')
    plt.ylabel('Goles del oponente')

    # Grafico de dispersion
    plt.subplot(1,2,2)
    sns.scatterplot(data= data,x= 'own_goals',y= 'opponent_goals')
    plt.title('Distribucion de goles propios vs goles del oponente')
    plt.xlabel('own')
    plt.ylabel('opponent')


    plt.tight_layout()
    plt.show()



    return muestra


#----------------------------------------------------------------------------------------------------


def victorias_como_locales(df):

    """Esta función analiza las victorias como local por club y grafica los 7 clubes con más victorias.

    Parámetros: df (DataFrame), DataFrame que contiene los datos de los partidos, incluyendo 
                    las columnas 'hosting', 'is_win' y 'club_id'.

    Retorna: DataFrame (DataFrame con los 7 clubes con más victorias como local).
    
    """
    ## para its_win:
    ## 0 = False
    ## 1 = True

    temp = df[(df['hosting'] == 'Home') & (df['is_win'] == 1)]
    temp = temp.groupby('club_id').agg({'is_win': 'sum'}).reset_index()
    data = temp.sort_values(by= 'is_win', ascending= False).nlargest(7, columns= 'is_win')
    data['club_id'] = data['club_id'].astype(str)

    #graficamos
    plt.figure(figsize= (16,8))
    sns.barplot(data= data, x= 'club_id', y= 'is_win')
    plt.title('Cantidad de Victorias como local por club')
    plt.xlabel('Club')
    plt.ylabel('Cantidad de Victorias')

    plt.show()

    return data


#----------------------------------------------------------------------------------------------------

def correlacion_posicion_x_goles_anotados(df):
 
    """Esta función toma un DataFrame y realiza un análisis de correlación entre 
    las posiciones de los jugadores y los goles anotados. La función crea 
    gráficos de dispersión y de densidad, y calcula las correlaciones de Pearson 
    y Spearman, presentando los resultados en mapas de calor.

    Parámetros:
    df (DataFrame): Un DataFrame que contiene las columnas 'own_position' y 'own_goals'.

    Retorna:
    DataFrame: El DataFrame filtrado utilizado en el análisis.
    
    """

    data = df[['own_position', 'own_goals']]
    data = data[data['own_position'] != -1] # recordemos que el valor -1 se utilizo para reemplazar valores nan, era donde faltaban valores para la categoria.

    plt.figure(figsize= (16,8))
    plt.subplot(2,1,1)
    sns.scatterplot(data= data, x= 'own_position', y= 'own_goals')
    plt.title('Grafico de dispersión y densidad own_position vs own_goals')
    plt.xlabel('Position')
    plt.ylabel('Goals')

    plt.subplot(2,1,2)
    sns.kdeplot(data= data, x= 'own_position', y= 'own_goals', fill= True, cbar= True)
    plt.tight_layout()
    plt.show()



    corr_pearson = data.corr()
    corr_spearman = data.corr(method= 'spearman')


    plt.figure(figsize= (16,8))
    plt.subplot(2,1,1)
    sns.heatmap(corr_pearson, annot= True, cmap= 'magma')
    plt.title('Grado de correlación Pearson (lineal)')


    plt.subplot(2,1,2)
    sns.heatmap(corr_spearman, annot= True, cmap= 'magma')
    plt.title('Grado de correlación Spearman (monotona)')

    plt.show()
    return data

#----------------------------------------------------------------------------------------------------
def etiquetas(valor1, valor2):

    """Función auxiliar que etiqueta el resultado del partido basado en los goles propios y del oponente.

    Parámetros:
    valor1 (int): Goles anotados por el propio equipo.
    valor2 (int): Goles anotados por el equipo oponente.

    Retorna:
    str: 'draw' si es un empate, 'win' si el propio equipo gana, 'lose' si el propio equipo pierde.
    
    """

    if valor1 - valor2 == 0:
        return 'draw'
    elif valor1 > valor2:
        return 'win'
    elif valor1 < valor2:
        return 'lose'

def resultado_partido_x_club(df):

    """Calcula y visualiza los resultados de los partidos por club.
    
    Args:
    df (pd.DataFrame): DataFrame con las columnas 'club_id', 'own_goals', y 'opponent_goals'.
    
    Returns:
    pd.DataFrame: DataFrame con los resultados calculados y proporciones.
    
    """
    
    df['results'] = df.apply(lambda row: etiquetas(row['own_goals'], row['opponent_goals']), axis= 1)
    # Contar los resultados por club
    data = df.groupby(['club_id', 'results']).size().unstack(fill_value=0).reset_index()
    data['draw_mean'] = data.apply(lambda row: round(row['draw'] / (row['draw'] + row['lose'] + row['win']) * 100, 2), axis= 1)
    data['win_mean'] = data.apply(lambda row: round(row['win'] / (row['draw'] + row['lose'] + row['win']) * 100, 2), axis= 1)
    data['lose_mean'] = data.apply(lambda row: round(row['lose'] / (row['draw'] + row['lose'] + row['win']) * 100, 2), axis= 1)
    data['total_games'] = data['draw'] + data['lose'] + data['win']
    data.sort_values(by= 'total_games', ascending= False, inplace= True)
    muestra = data.iloc[0:7]

    # Crear el gráfico de barras agrupadas
    muestra.set_index('club_id')[['draw', 'lose', 'win']].plot(kind='bar', stacked=False, figsize=(12, 8))
    plt.title('Resultados de los partidos por club')
    plt.xlabel('Club ID')
    plt.ylabel('Número de Partidos')
    plt.xticks(rotation=0)
    plt.legend(title='Resultados')

    plt.tight_layout()
    plt.grid()
    plt.show()

    return data
#----------------------------------------------------------------------------------------------------

def rendimiento_entrenadores(df):

    """ Esta función calcula el rendimiento de los entrenadores por club,
    mostrando el número de partidos ganados en casa y fuera de casa,
    y un gráfico adicional con la distribución de partidos por localía y resultado.

    Parámetros:
    df (DataFrame): DataFrame que contiene los datos de los partidos.

    Retorna:
    data (DataFrame): DataFrame con el número de partidos ganados en casa y fuera de casa por cada entrenador.
    
    
    """

    temp = df[['own_manager_name', 'hosting', 'is_win']]
    data = temp[temp['is_win'] == 1].groupby(['own_manager_name', 'hosting']).size().unstack(fill_value= 0).reset_index()
    muestra = data.iloc[0:7]

    # Crear el gráfico de barras agrupadas
    muestra.set_index('own_manager_name')[['Home', 'Away']].plot(kind='bar', stacked=False, figsize=(12, 8))
    plt.title('Rendimiento de entrenadores por club por localia')
    plt.xlabel('Manager_name')
    plt.ylabel('Número de Partidos')
    plt.xticks(rotation=0)
    plt.legend(title='Resultados')
    plt.grid()
    plt.show()

    plt.figure(figsize= (16,8))
    sns.countplot(data= temp, x= 'hosting', hue= 'is_win')
    plt.title('Rendimiento por localia')
    plt.xlabel('Hosting')
    plt.ylabel('Número de Partidos')
    plt.xticks(rotation=0)
    plt.legend(title='Is win')
    plt.grid()


    plt.tight_layout()
    plt.show()



    return data

#----------------------------------------------------------------------------------------------------

def ():
    return


#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------

def main():
    
    return

if __name__ == '__main__':
    main()