from bottle import get, post, run, request, response
import sqlite3


db = sqlite3.connect("database.sqlite")


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
        VALUES    ('Kino', 10), ('Regal', 16), ('Skandia', 100);
        """
    )
    response.status = 201
    db.commit()


@post('/users')
def post_users():
    user = request.json
    c = db.cursor()
    try:
        c.execute(
            """
            INSERT
            INTO customers(username, name, password)
            VALUES (?, ?, ?)
            """,
            [user['username'], user['fullName'], user['pwd']]
        )
        response.status = 201
        db.commit()
        return {"/users/" + user['username']}
    except:
        response.status = 400
        return {""}


@post('/movies')
def post_movies():
    movie = request.json
    c = db.cursor()
    try:
        c.execute(
            """
            INSERT
            INTO movies(imdb_key, title, year)
            VALUES (?, ?, ?)
            """,
            [movie['imdbKey'], movie['title'], movie['year']]
        )
        response.status = 201
        db.commit()
        return {"/movies/" + movie['imdbKey']}
    except:
        response.status = 400
        return {""}


@post('/performances')
def post_performances():
    performance = request.json
    c = db.cursor()
    try:
        c.execute(
            """
            INSERT
            INTO screenings(t_name, imdb_key, date, start)
            VALUES (?,?,?,?)
            """,
            [performance['theater'], performance['imdbKey'], performance['date'], performance['time']]
        )
        db.commit()
        c.execute(
            """
            UPDATE screenings
            SET seats = (SELECT capacity FROM theaters WHERE ? IS t_name)
            WHERE imdb_key IS ? AND date IS ? AND start IS ? AND t_name IS ?
            """,
            [performance['theater'], performance['imdbKey'], performance['date'], performance['time'], performance['theater']]
        )
        db.commit()
        c.execute(
            """
            SELECT  screen_id
            FROM    screenings
            WHERE   rowid = last_insert_rowid()
            """
        )
        found = [screen_id for screen_id in c]
        response.status = 201
        db.commit()
        return {"/performances/" + found[0][0]}
    except:
        response.status = 400
        return {"No such movie or theater"}


@get('/movies')
def get_movies():
    c = db.cursor()
    c.execute(
        """
        SELECT  imdb_key, title, year
        FROM    movies
        """
    )
    found = [{"imdbKey": imdb_key, "title": title, "year": year} for imdb_key, title, year in c]
    response.status = 200
    return {"data": found}


@get('/movies/<title, year>')
def get_movie(title, year):
    c = db.cursor()
    c.execute(
        """
        SELECT  imdb_key, title, year
        FROM    movies
        WHERE   title LIKE ? AND year LIKE ?
        """,
        [title, year]
    )
    found = [{"imdbKey": imdb_key, "title": title, "year": year} for imdb_key, title, year in c]
    response.status = 200
    return {"data": found}


@get('/movies/<imdb_key>')
def get_movie(imdb_key):
    c = db.cursor()
    c.execute(
        """
        SELECT  imdb_key, title, year
        FROM    movies
        WHERE   imdb_key LIKE ?
        """,
        [imdb_key]
    )
    found = [{"imdbKey": imdb_key, "title": title, "year": year} for imdb_key, title, year in c]
    response.status = 200
    return {"data": found}


@get('/performances')
def get_performances():
    c = db.cursor()
    c.execute(
        """
        SELECT  screen_id, date, start, title, year, t_name, seats
        FROM    screenings
        JOIN    movies
        USING   (imdb_key)
        """
    )
    found = [{"performanceId": screen_id, "date": date, "startTime": start, "title": title, "year": year, "theater": t_name, "remainingSeats" : seats} for screen_id, date, start, title, year, t_name, seats in c]
    response.status = 200
    return {"data": found}


@post('/tickets')
def post_tickets():
    user = request.json
    c = db.cursor()
    try:
        c.execute(
            """
            SELECT username, password
            FROM customers
            WHERE username LIKE ? AND password LIKE ?
            """,
            [user['username'], user['pwd']]
        )
        if not c.fetchall():
            response.status = 401
            return {"Wrong user credentials"}
        c.execute(
            """
            SELECT seats
            FROM screenings
            WHERE ? IS screen_id
            """,
            [user['performanceId']]
        )
        if c.fetchone()[0] == 0:
            response.status = 400
            return {"No tickets left"}
        c.execute(
            """
            INSERT
            INTO tickets(username, screen_id)
            VALUES (?, ?)
            """,
            [user['username'], user['performanceId']]
        )
        c.execute(
            """
            UPDATE screenings
            SET seats = seats-1
            WHERE ? IS screen_id
            """,
            [user['performanceId']]
        )
        db.commit()
        response.status = 201
        return {"/tickets/" + user['performanceId']}
    except:
        response.status = 400
        return {"Error"}


@get('/users/<username>/tickets')
def get_tickets(username):
    c = db.cursor()
    c.execute(
        """
        SELECT  *, count() AS nbrOfTickets
        FROM    customers
        JOIN    tickets
        USING   (username)
        WHERE   username = ?
        GROUP BY screen_id
        """,
        [username]
    )
    print(c.fetchall())
    found = [{"date": date, "startTime": start, "theater": t_name, "title": title, "year" : year, "nbrOfTickets" : nbrOfTickets} for date, start, t_name, title, year, nbrOfTickets in c]
    response.status = 200
    return {"data": found}


run(host='localhost', port=7007)
