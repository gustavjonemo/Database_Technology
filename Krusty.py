from bottle import get, post, run, request, response
import sqlite3
from urllib.parse import quote, unquote


db = sqlite3.connect("database.sqlite")

@post('/reset')
def reset():
    c = db.cursor()
    c.executescript(
        """
        DELETE FROM Cookie_ingredients;
        DELETE FROM Material_storage;
        DELETE FROM Cookies;
        DELETE FROM Order_details;
        DELETE FROM Customers;
        DELETE FROM Pallets;
        DELETE FROM Orders;
        DELETE FROM Deliveries;
        """
    )
    response.status = 205
    db.commit()
    return {"location": "/"}


@post('/customers')
def post_customers():
    customer = request.json
    c = db.cursor()
    try:
        c.execute(
            """
            INSERT
            INTO Customers(customer_name, address)
            VALUES (?, ?)
            """,
            [customer['name'], customer['address']]
        )
        response.status = 201
        db.commit()
        return {"location": "/customers/" + quote(customer['name'])}
    except:
        response.status = 400
        return {""}


@get('/customers')
def get_customers():
    c = db.cursor()
    c.execute(
        """
        SELECT  customer_name, address
        FROM    Customers
        """
    )
    found = [{"name": customer_name, "address": address} for customer_name, address in c]
    response.status = 200
    return {"data": found}


@post('/ingredients')
def post_ingredients():
    ingredient = request.json
    c = db.cursor()
    try:
        c.execute(
            """
            INSERT
            INTO Material_storage(ingredient, unit, current_amount)
            VALUES (?, ?, 0)
            """,
            [ingredient['ingredient'], ingredient['unit']]
        )
        response.status = 201
        db.commit()
        return {"location": "/ingredients/" + quote(ingredient['ingredient'])}
    except:
        response.status = 400
        return {""}


@post('/ingredients/<ingredients>/deliveries')
def post_ingredients(ingredients):
    ingredient = request.json
    c = db.cursor()
    try:
        c.execute(
            """
            UPDATE Material_storage
            SET delivery_time = ?,
                current_amount =current_amount + ?,
                last_deposit = ?
            WHERE ingredient LIKE ?
            """,
            [ingredient['deliveryTime'], ingredient['quantity'], ingredient['quantity'], ingredients]
        )
        response.status = 201
        db.commit()
        found = [{"ingredient": ingredient, "quantity": current_amount, "unit": unit} for ingredient, current_amount, unit in c]
        return {"data": found}
    except:
        response.status = 400
        return {""}


@get('/ingredients')
def get_ingredients():
    c = db.cursor()
    try:
        c.execute(
            """
            SELECT ingredient, current_amount, unit
            FROM Material_storage
            """
        )
        response.status = 201
        db.commit()
        found = [{"ingredient": ingredient, "quantity": current_amount, "unit": unit} for ingredient, current_amount, unit in c]
        return {"data": found}
    except:
        response.status = 400
        return {""}


@post('/cookies')
def post_cookies():
    cookie = request.json
    recipe = [(cookie["name"], x["ingredient"], x["amount"]) for x in cookie["recipe"]]
    c = db.cursor()
    try:
        c.execute(
            """
            INSERT
            INTO Cookies(cookie_name)
            VALUES (?)
            """,
            [cookie['name']]
        )
        db.commit()
        c.executemany(
            """
            INSERT
            INTO Cookie_ingredients(cookie_name, ingredient, amount)
            VALUES (?,?,?);
            """,
            recipe
        )
        response.status = 201
        db.commit()
        return {"location": "/cookies/" + quote(cookie['name'])}
    except:
        response.status = 400
        return {""}


@get('/cookies')
def get_cookies():
    c = db.cursor()
    try:
        c.execute(
            """
            SELECT cookie_name, count(blocked) as unblocked_pallets
            FROM Cookies
            JOIN Pallets
            USING (cookie_name)
            WHERE blocked IS 0
            GROUP BY cookie_name
            """
        )
        response.status = 200
        db.commit()
        found = [{"name": cookie_name, "pallets": unblocked_pallets} for cookie_name, unblocked_pallets in c]
        print(found)
        return {"data": found}
    except:
        response.status = 400
        return {""}


@get('/cookies/<cookie_name>/recipe')
def get_cookies(cookie_name):
    c = db.cursor()
    try:
        c.execute(
            """
            SELECT  ingredient, amount, unit
            FROM    Cookie_ingredients
            JOIN    Material_storage
            USING   (ingredient)
            WHERE   cookie_name = ?
            """,
            [cookie_name]
        )
        found = [{"ingredient": ingredient, "amount": amount, "unit": unit} for ingredient, amount, unit in c]
        if found:
            response.status = 200
        else:
            response.status = 404
        return {"data": found}
    except:
        response.status = 404 
        return {"data": []}


@post('/cookies/<cookie_name>/block')
def get_cookies(cookie_name):

    try:
        query = """
        UPDATE Pallets
        SET blocked = 1
        WHERE cookie_name IS ?
        """
        params = [cookie_name]
        if request.query.after:
            query += "AND date(pallet_time) > ?"
            params.append(request.query.after)
        if request.query.before:
            query += "AND date(pallet_time) < ?"
            params.append(request.query.before)
        c = db.cursor()
        c.execute(query, params)
        db.commit()
        response.status = 205
        return {""}
    except:
        response.status = 404
        return {"could not block pallets"}\

@post('/cookies/<cookie_name>/unblock')
def get_cookies(cookie_name):
    c = db.cursor()
    try:
        query = """
        UPDATE Pallets
        SET blocked = 0
        WHERE cookie_name IS ?
        """
        params = [cookie_name]
        if request.query.after:
            query += "AND date(pallet_time) > ?"
            params.append(request.query.after)
        if request.query.before:
            query += "AND date(pallet_time) < ?"
            params.append(request.query.before)
        c.execute(query, params)
        db.commit()
        response.status = 205
        return {""}
    except:
        response.status = 404
        return {"could not block pallets"}


@post('/pallets')
def post_pallets():
    pallet = request.json
    c = db.cursor()
    try:
        c.execute(
            """
            INSERT
            INTO Pallets(cookie_name, pallet_time, delivery_status, blocked)
            VALUES (?, DATETIME("NOW"), 0, 0)
            """,
            [pallet['cookie']]
        )
        db.commit()
        c.execute(
            """
            SELECT pallet_id
            FROM Pallets
            WHERE rowid = last_insert_rowid()
            """
        )
        response.status = 201
        id = c.fetchone()[0]
        return {"location": "/pallets/" + id}
    except:
        response.status = 422
        return {"location": ""}


@get('/pallets')
def get_pallets():
    try:
        query = """
        SELECT  pallet_id, cookie_name, pallet_time, blocked
        FROM    Pallets
        WHERE 1 = 1
        """
        params = []
        if request.query.cookie:
            query += "AND cookie_name = ?"
            params.append(request.query.cookie)
        if request.query.after:
            query += "AND date(pallet_time) > ?"
            params.append(request.query.after)
        if request.query.before:
            query += "AND date(pallet_time) < ?"
            params.append(request.query.before)
        c = db.cursor()
        if(params):
            c.execute(query, params)
        else:
            c.execute(query)


        found = [{"id": pallet_id, "cookie": cookie_name, "productionDate": pallet_time.split()[0], "blocked": blocked} for pallet_id, cookie_name, pallet_time, blocked in c]
        if found:
            response.status = 200
        else:
            response.status = 404
        return {"data": found}
    except:
        response.status = 404
        return {"data": []}


run(host='localhost', port=8888)