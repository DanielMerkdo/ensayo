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
                         
------crear tablas filtradas de  peliculas, usuarios y calificaciones ----


drop table if exists ratings_final;

create table ratings_final as
select a."userId"as user_id,
a.movieId as movie_Id,
a."rating" as movie_rating,
a."timestamp" as rating_time
from ratings a 
inner join movies_sel b
on a.movieId =b.movieId
inner join usuarios_sel c
on a."userId" =c.user_id;



-- VERIFICAR CODIGO ABAJO

drop table if exists movies_final;

create table movies_final as
select a.movieId as movie_id,
a."title"  as movie_title,
a."genres" as movie_genre
from movies a
inner join movies_sel c
on a.movieId= c.movieId;



---crear tabla completa ----

drop table if exists full_ratings ;

create table full_ratings as select 
a.*,
c.movie_title,
c.movie_genre
from ratings_final a inner join
movies_final c on a.movie_Id=c.movie_Id;