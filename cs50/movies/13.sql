SELECT DISTINCT(people.name) FROM  people
JOIN stars ON stars.person_id = people.id
JOIN movies ON movies.id = stars.movie_id
WHERE movies.id IN (
SELECT movies.id from movies
JOIN stars on stars.movie_id = movies.id
JOIN people ON people.id = stars.person_id
WHERE people.name LIKE "Kevin Bacon") AND people.name NOT LIKE "Kevin Bacon";