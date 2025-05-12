import pandas as pd
import numpy as np
import sqlite3 

   
def ejecutar_sql (nombre_archivo, cur):
    sql_file=open(nombre_archivo)
    sql_as_string=sql_file.read()
    sql_file.close
    cur.executescript(sql_as_string)

def recommendation(model, data, original_user_id, conex,k):

  #data=dataset_train
  #original_user_id=1

  ## peliculas no leidos y códigos
  df_nr_movies=pd.read_sql(f'select * from db_movies_final where user_id<>{original_user_id}',conex)
  movieid_nr_movies=df_nr_movies['movie_Id'].values
  item_id_nr=[value for key, value in data.mapping()[2].items() if value not in movieid_nr_movies]

  uid_index=data.mapping()[0][original_user_id] ## id usuario según modelo

  scores=model.predict(uid_index, item_id_nr)
  sorted_indices = np.argsort(-scores).tolist()

  top_items = [key for key, value in data.mapping()[2].items() if value in sorted_indices[:k]]
  recommended=df_nr_movies[df_nr_movies['movie_Id'].isin(top_items)][['movie_Id', 'movie_title']]
  recommended.drop_duplicates(inplace=True)

  return recommended
    

