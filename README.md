<p align="center">
  <img src="assets/Logo_consultora.png" width="50%" alt="consultora">
</p>

# <h1 align= 'center'>Estudio y desarrollo de aplicación sobre Rendimiento Deportivo </h1>

![Markdown](https://img.shields.io/badge/-Markdown-black?style=flat-square&logo=markdown)
![Python](https://img.shields.io/badge/-Python-black?style=flat-square&logo=python)
![Numpy](https://img.shields.io/badge/-Numpy-black?style=flat-square&logo=numpy)
![Pandas](https://img.shields.io/badge/-Pandas-black?style=flat-square&logo=pandas)
![Matplotlib](https://img.shields.io/badge/-Matplotlib-black?style=flat-square&logo=matplotlib)
![Seaborn](https://img.shields.io/badge/-Seaborn-black?style=flat-square&logo=seaborn)
![Scikitlearn](https://img.shields.io/badge/-Scikitlearn-black?style=flat&logo=scikitlearn)
![AWS](https://img.shields.io/badge/-AWS-black?style=flat-square&logo=aws)
![Power BI](https://img.shields.io/badge/-Power%20BI-black?style=flat-square&logo=powerbi)
![Git](https://img.shields.io/badge/-Git-black?style=flat-square&logo=git)
![GitHub](https://img.shields.io/badge/-GitHub-black?style=flat-square&logo=github)
![Google Drive](https://img.shields.io/badge/-Google%20Drive-black?style=flat-square&logo=googledrive)
![Google Colaboratory](https://img.shields.io/badge/-Google%20Colaboratory-black?style=flat-square&logo=googlecolaboratory)
![Jupyter](https://img.shields.io/badge/-Jupyter-black?style=flat&logo=jupyter)
![Visual Studio Code](https://img.shields.io/badge/-Visual%20Studio%20Code-black?style=flat&logo=visual-studio-code&logoColor=007ACC)

# Índice

- [Descripción](#Descripción)
- [Introducción](#Introducción)
- [Objetivos](#Objetivos)
- [Datos](#Datos)
- [Desarrollo](#Desarrollo)
  - [ETL](#ETL)
  - [EDA](#EDA)
  - [Dashboard](#Dashboard)
  - [Modelo](#Modelo)
  - [Deploy](#Deploy)
- [Tecnologías](#Tecnologías)
- [Documentación](#Documentación)
- [Equipo](#Equipo)

# Descripción

Este proyecto forma parte de una simulación laboral realizada por NoCountry en donde se toma una temática o tema para generar el desarrollo de un proyecto como solución a una problematica de negocio basada en datos.

La temática del proyecto elegida en este caso, esta referida al rendimiento deportivo de equipos de futbol; enfocada en un contexto general de rendimiento en una competencia, y en particular en un evento o partido.


# Introducción

<p align="center">
  <img src="assets/Banner_DeRabona.png" width="70%" alt="consultora">
</p>

La plataforma DeRabona es un sitio web que contiene informacion futbolística, como puntuaciones, resultados, estadísticas, noticias sobre transferencias y partidos. 

A pesar de que los valores de los jugadores, junto con otros hechos, son estimaciones, investigadores del Center for Economic Performance han descubierto que los "rumores" sobre transferencias de jugadores son en gran medida exactos.

Estos valores estimados de los jugadores generalmente se actualizan cada pocos meses; considerando cómo funciona el mercado del fútbol de asociación , estas estimaciones pueden ser ligeramente inferiores o superiores a lo que podría sugerir la forma actual de los jugadores y, por lo tanto, el valor actual.

Una apuesta deportiva es un pronóstico de un evento o de un resultado deportivo puntual que consiste en apostar una determinada cantidad de dinero por el resultado elegido.

El proposito de una apuesta deportiva es beneficiarse de este pronóstico o predicción entonces, si se acierta el pronostico que se hizo, cobrarás tus ganancias.

La industria de las apuestas deportivas continúa en franco ascenso y Argentina no es la excepción ante esta tendencia global. De hecho, un reciente informe en la región indica que el rubro ya genera aproximadamente 10 mil millones de dólares en Latinoamérica, de los cuales casi un 25% (2,4 mil millones) corresponden al país campeón mundial de fútbol.

Según indica la compañía Playtech, encargada de llevar a cabo el relevamiento en territorio albiceleste pero que también incluyó a Brasil, Perú, Chile y Colombia, el crecimiento despegó en particular a partir de la pandemia de Covid-19 y los argentinos lideran este incremento en cuanto a cantidad de usuarios registrados y descargas de aplicaciones. 

# Objetivos

Nuestro cliente, dueño del sitio DeRabona nos pide que se realice un estudio sobre el rendimiento deportivo en general para identificar informacion valiosa para 
encarar nuevas funcionalidades e identificar patrones fundamentales en la dinamica de los equipos, jugadores, torneos, etc.

Tambien, se nos encarga la creacion de una aplicacion o sistema que permita predecir o pronosticar el resultado de un partido determinado, con miras al desarrollo de una aplicacion y seccion de apuestas en el sitio basandose en el contexto de desarrollo y crecimiento pronunciado en la industria de las apuestas deportivas en todo el mundo y en especial, en Latinoamerica.

# Datos

Los datos utilizados, provienen de dos fuentes:

* Transfermarkt
* Kaggle

Los datos extraidos de Kaggle estan integrados por 9 ficheros con formato csv, los cuales contienen data referente a clubes, competencias y jugadores de futbol.
Estos son:

* appearances
* club_games
* clubs
* competitions
* game_events
* game_lineups
* games
* player_valuations
* players

Aunque estos ficheros son extraidos de kaggle, originalmente contienen datos de la plataforma Transfermarket. Por lo que decidimos complementar estos ficheros extrayendo desde la plataforma datos sobre una liga en particular, en este caso la liga de Brasil o el Brasileirao, para complementar nuestros datos y tener un contraste con lo cual comparar nuestra data original y tambien con la cual probar distintos análisis, postulados, y modelos que constuyamos a lo largo del desarrollo del proyecto.
Esta data se descargo en una carpeta comprimida, archivos json liga brasil.zip, la cual cuenta con los siguientes ficheros:

* clubs
* game_lineups
* games
* players

Disponibilizamos el diccionario de datos de nuestra data [aquí]()

# Desarrollo

## ETL

En la fase de Transformación de Datos (ETL), se llevaron a cabo una serie de procedimientos para garantizar la preparación adecuada y la limpieza exhaustiva de los datos antes de su carga en el almacén de datos. Estas acciones incluyeron:

Verificación del tipo de datos de cada columna: Se examinó minuciosamente el tipo de datos de cada columna para garantizar su coherencia y precisión en el análisis posterior.
Análisis de la dimensionalidad de los datos: Se exploró la estructura del conjunto de datos para comprender su tamaño y complejidad, lo que permitió una mejor comprensión de la cantidad de registros y variables presentes.
Manejo de valores nulos: Se identificaron y abordaron los valores nulos en el conjunto de datos mediante técnicas como la imputación de datos o la eliminación de registros incompletos, con el fin de evitar sesgos o distorsiones en el análisis posterior.
Verificación visual de valores atípicos: Se realizó una exploración gráfica de los datos para detectar posibles valores atípicos o anomalías que podrían afectar la integridad y la precisión de los resultados.
Indagación de consistencia de los datos: Se llevaron a cabo investigaciones exhaustivas sobre la consistencia de los datos, incluyendo la identificación de máximos, mínimos y rangos de valores para cada variable, lo que ayudó a garantizar la fiabilidad de los datos utilizados en el análisis.
El Informe ETL proporciona un análisis detallado de la calidad y las características de los datos originales, y ofrece funciones específicas para examinar y explorar los datos en profundidad. Estas funciones incluyen la visualización de valores nulos, análisis de frecuencia de palabras, boxplots numéricos y más, lo que facilita la identificación de patrones, tendencias y relaciones significativas en los datos.

## EDA

El proceso de Preparación de Datos comenzó con una exhaustiva limpieza y preprocesamiento para garantizar la calidad y coherencia de los datos recopilados. Posteriormente, se llevó a cabo un Análisis Exploratorio de Datos, utilizando técnicas estadísticas y herramientas de visualización para comprender la estructura y distribución de los datos, identificando patrones, tendencias y relaciones entre las variables.

En el Análisis Descriptivo, se examinaron diversas variables

## Dashboard

Disponibilizamos el link de nuestro dashboard aquí [link al repositorio externo](https://drive.google.com/file/d/1CdmsJfXDvFW8jB-WrEXQD3SqSRz-swcC/view?usp=drive_link)
## Modelo
## Deploy

# Tecnologías

* ![Markdown](https://img.shields.io/badge/-Markdown-black?style=flat&logo=markdown)
* ![Python](https://img.shields.io/badge/-Python-black?style=flat-square&logo=Python)
* ![Pandas](https://img.shields.io/badge/-Pandas-black?style=flat&logo=pandas)
* ![Numpy](https://img.shields.io/badge/-Numpy-black?style=flat&logo=numpy)
* ![Matplotlib](https://img.shields.io/badge/-Matplotlib-black?style=flat&logo=matplotlib)
* ![Seaborn](https://img.shields.io/badge/-Seaborn-black?style=flat&logo=seaborn)
* ![Scikitlearn](https://img.shields.io/badge/-Scikitlearn-black?style=flat&logo=scikitlearn)
* ![PowerBI](https://img.shields.io/badge/-PowerBI-black?style=flat&logo=powerbi)
* ![PowerQuery](https://img.shields.io/badge/-PowerQuery-black?style=flat&logo=powerquery)
* ![AWS](https://img.shields.io/badge/-AWS-black?style=flat-square&logo=aws)
* ![Git](https://img.shields.io/badge/-Git-black?style=flat-square&logo=git)
* ![GitHub](https://img.shields.io/badge/-GitHub-black?style=flat-square&logo=github)
* ![Jupyter](https://img.shields.io/badge/-Jupyter-black?style=flat&logo=jupyter)
* ![colab](https://img.shields.io/badge/-colab-black?style=flat&logo=colabbadge)
* ![Visual Studio Code](https://img.shields.io/badge/-Visual%20Studio%20Code-black?style=flat&logo=visual-studio-code&logoColor=007ACC)


# Documentacion

Ponemos a disposición la documentación del desarrollo integral del proyecto, como informe de presentacion empresarial, para el entendimiento del enfoque principal, el desarrollo, la metodología y las diferentes etapas recorridas en el análisis de los datos y la construcción de los insights. Podemos ver la documentacion completa de nuestro proyecto [aquí](docs/Documentacion_AyC_DeRabona.docx)

# Equipo

<div align="center">

<!-- Primera fila -->
<table>
  <tr>
    <td align="center">
      <img src="https://avatars.githubusercontent.com/u/106486985?s=400&u=f2b5a4953b674b71e5df9e4c71c89ee2ae75fa65&v=4" width="200" height="200"><br><strong>Marco</strong><br>
      <a href="https://www.linkedin.com/in/marco-antonio-caro-22459711b"><img src="assets/linkedin.png" style="width:20px;"></a>
      <a href="https://github.com/marco11235813"><img src="assets/github.png" style="width:20px;"></a>
    </td>
    <td align="center">
      <img src="https://avatars.githubusercontent.com/u/125699535?v=4" width="200" height="200"><br><strong>Adrian</strong><br>
      <a href="http://www.linkedin.com/in/juan-manuel-yunes-mor"><img src="assets/linkedin.png" style="width:20px;"></a>
      <a href="https://github.com/jyunesmor"><img src="assets/github.png" style="width:20px;"></a>
    </td>
    <td align="center">
      <img src="https://avatars.githubusercontent.com/u/101422922?v=4" width="200" height="200"><br><strong>Guillermo</strong><br>
      <a href="http://www.linkedin.com/in/leandro-mambelli-79834a6b"><img src="assets/linkedin.png" style="width:20px;"></a>
      <a href="https://github.com/guillermo"><img src="assets/github.png" style="width:20px;"></a>
    </td>
  </tr>
</table>

<!-- Segunda fila -->
<table>
  <tr>
    <td align="center">
      <img src="https://avatars.githubusercontent.com/u/112107967?v=4" width="200" height="200"><br><strong>Jorge</strong><br>
      <a href="https://www.linkedin.com/in/jorge-antonio"><img src="assets/linkedin.png" style="width:20px;"></a>
      <a href="https://github.com/jorge11235813"><img src="assets/github.png" style="width:20px;"></a>
    </td>
    <td align="center">
      <img src="https://avatars.githubusercontent.com/u/108310078?v=4" width="200" height="200"><br><strong>Matias</strong><br>
      <a href="http://www.linkedin.com/in/matias"><img src="assets/linkedin.png" style="width:20px;"></a>
      <a href="https://github.com/matias"><img src="assets/github.png" style="width:20px;"></a>
    </td>
  </tr>
</table>

</div>

