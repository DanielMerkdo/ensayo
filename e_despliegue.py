import numpy as np
import pandas as pd
import sqlite3 as sql
import openpyxl


####Paquete para sistema basado en contenido ####
from sklearn.preprocessing import MinMaxScaler
from sklearn import neighbors

import a_funciones as funciones     # Importar las funciones
import importlib
importlib.reload(funciones)

####Paquete para sistema basado en contenido ####
from sklearn.preprocessing import MinMaxScaler
from sklearn import neighbors

import logging
from tqdm import tqdm

# Conffiguración del logg
logging.basicConfig(
    filename='G:\\Mi unidad\\cod\\analitica_marketing\\salida\\reco\\script_log.log',
    level=logging.INFO,       #nivel de logg, informativo solo muestra informació básica de ejecución
    format='%(asctime)s - %(levelname)s - %(message)s'  ## formato log, hora, nievel(error, informativo, advertencia), mensaje personalizado cuando se llama logg
)

def preprocesar(conex=None, cur=None):

    ######## convertir datos crudos a bases filtradas por usuarios que tengan cierto número de calificaciones
    #funciones.ejecutar_sql('G:\\Mi unidad\\cod\\analitica_marketing\\preprocesamiento.sql', cur)

    log_mes='Ejecución de SQL para filtrar peliculas y ratings completada.'
    logging.info(log_mes)
    print(log_mes)

    ##### llevar datos que cambian constantemente a python ######
    movies1=pd.read_sql("""select * from db_movies_final""", conex)
    ratings=pd.read_sql("""select * from db_movies_final""", conex)
    usuarios=pd.read_sql('select distinct (user_id) as user_id from db_movies_final',conex)

    #### transformación de datos crudos - Preprocesamiento ################

    # Se eliminan los registros duplicados, solo se requiere el catalogo de las peliculas
    movies2= movies1.drop_duplicates(subset='movie_Id', keep='first').reset_index(drop=True)

    ##### escalar para que año esté en el mismo rango ###
    sc=MinMaxScaler()
    movies2[["movie_yearsc"]]=sc.fit_transform(movies2[['movie_year']])

    #eliminar columnas que no se requieren para el analisis
    movies3=movies2.drop(columns=['user_id','movie_Id','movie_rating','movie_year','rating_year','movie_title'])


    log_mes='Preprocesamiento de datos completado.'
    logging.info(log_mes)
    print(log_mes)

    return movies3,movies2, conex, cur


##########################################################################
###############Función para entrenar modelo por cada usuario ##########
###############Basado en contenido todo lo visto por el usuario Knn#############################
def recomendar(user_id, conex=None, cur=None, movies3=None, movies2=None):

    ratings=pd.read_sql('select *from db_movies_final where user_id=:user',conex, params={'user':user_id})
    l_movies_r=ratings['movie_Id'].to_numpy()
    movies3[['movie_Id','movie_title']]=movies2[['movie_Id','movie_title']]
    movies_r=movies3[movies3['movie_Id'].isin(l_movies_r)]
    movies_r=movies_r.drop(columns=['movie_Id','movie_title'])
    movies_r["indice"]=1 ### para usar group by y que quede en formato pandas tabla de centroide
    centroide=movies_r.groupby("indice").mean()

    log_mes=f'Generando recomendaciones para el usuario {user_id}.'
    logging.info(log_mes)
    print(log_mes)


    movies_nr=movies3[~movies3['movie_Id'].isin(l_movies_r)]
    movies_nr=movies_nr.drop(columns=['movie_Id','movie_title'])
    model=neighbors.NearestNeighbors(n_neighbors=11, metric='cosine')
    model.fit(movies_nr)
    dist, idlist = model.kneighbors(centroide)

    ids=idlist[0]
    recomend_b=movies2.loc[ids][['movie_title','movie_Id']]

    log_mes=f'Recomendaciones para el usuario {user_id} finalizadas'
    logging.info(log_mes)
    print(log_mes)

    return recomend_b

##### Generar recomendaciones para usuario lista de usuarios ####
##### No se hace para todos porque es muy pesado #############
def main(list_user):

    #### conectar_base_de_Datos#################
    conex=sql.connect('G:\\Mi unidad\\cod\\analitica_marketing\\data\\db_movies_final.db')
    cur=conex.cursor()

    log_mes='Conexión a la base de datos establecida.'
    logging.info(log_mes)
    print(log_mes)

    recomendaciones_todos=pd.DataFrame()

    movies3, movies2, conex, cur= preprocesar(conex, cur)
    for user_id in tqdm(list_user):

        recomendaciones=recomendar(user_id, conex, cur, movies3, movies2)
        recomendaciones["user_id"]=user_id
        recomendaciones.reset_index(inplace=True,drop=True)

        recomendaciones_todos=pd.concat([recomendaciones_todos, recomendaciones])

    recomendaciones_todos.to_excel('G:\\Mi unidad\\cod\\analitica_marketing\\salida\\reco\\recomendaciones.xlsx')
    recomendaciones_todos.to_csv('G:\\Mi unidad\\cod\\analitica_marketing\\salida\\reco\\recomendaciones.csv')

    log_mes='Recomendaciones generadas y guardadas en Excel y CSV.'
    logging.info(log_mes)
    print(log_mes)

if __name__=="__main__":
  list_user=[2,50,120,308]
  main(list_user)

import sys
sys.executable