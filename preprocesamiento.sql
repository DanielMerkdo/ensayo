-- Preprocesamiento


-- Crear tabla con usuarios que calificaron mas de 20 películas y menos de 400
drop table if exists usuarios_sel;

create table usuarios_sel as 

select "userId" as user_id, count(*) as cnt_rat
from ratings
group by "userId"
having cnt_rat >20 and cnt_rat <= 400
order by cnt_rat desc ;

-- Crear tabla con peliculas que tengan más de 5 calificaciones 
drop table if exists movies_sel;


create table movies_sel as select movieId,
                         count(*) as cnt_rat
                         from ratings
                         group by movieId
                         having cnt_rat >5
                         order by cnt_rat desc ;
                         
------crear tablas filtradas de libros, usuarios y calificaciones ----