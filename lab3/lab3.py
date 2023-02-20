from bottle import get, post, run, request, response
import sqlite3


db = sqlite3.connect("movies.sqlite")


@get('/ping')
def ping():
    response.status = 200
    return {"pong"}


@post('/reset')
def reset():
    c = db.cursor()
    c.executescript(
        """
        DELETE FROM theaters;
        DELETE FROM movies;
        DELETE FROM screenings;
        DELETE FROM customers;
        DELETE FROM tickets; 
        INSERT
        INTO theaters(t_name, capacity)
        VALUES	('Kino', 10), ('Regal', 16), ('Skandia', 100);
        """
    )
    response.status = 201
    db.commit()


@post('/users')
def post_users():
    user = request.json
    c = db.cursor()
    c.execute(
        """
        INSERT
        INTO    customer(username, name, password)
        VALUES  (?, ?, ?);
        """,
        [user['username'], user['name'], user['password']]
    )
    response.status = 201
    db.commit()


run(host='localhost', port=7007)