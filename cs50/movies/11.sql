SELECT movies.title FROM movies 
JOIN stars ON stars.movie_id = movies.id
JOIN ratings ON stars.movie_id = ratings.movie_id
JOIN people ON Stars.person_id = people.id
WHERE people.name LIKE "Chadwick Boseman" ORDER BY ratings.rating DESC LIMIT 5;
