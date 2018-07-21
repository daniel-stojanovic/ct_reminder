INSERT INTO clients(internal_name)
VALUES (%(internal_name)s)
RETURNING id;