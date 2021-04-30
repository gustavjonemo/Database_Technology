PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS Cookie_ingredients;

CREATE TABLE Cookie_ingredients(
	cookie_name TEXT,
    ingredient  TEXT,
    amount      INT,
    FOREIGN KEY(cookie_name) REFERENCES Cookies(cookie_name)
);

DROP TABLE IF EXISTS Material_storage;

CREATE TABLE Material_storage(
	ingredient      TEXT PRIMARY KEY,
    current_amount  INT,
    delivery_time   DATETIME,
    last_deposit    INT,
    unit            TEXT
);

DROP TABLE IF EXISTS Cookies;

CREATE TABLE Cookies(
	cookie_name     TEXT PRIMARY KEY
);

DROP TABLE IF EXISTS Pallets;

CREATE TABLE Pallets(
	pallet_id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
	cookie_name TEXT,
    pallet_time DATETIME,
	delivery_status INT,  -- 1 - Delivered, 0 - Not delivered
	blocked INT,        -- 1 - Blocked, 0 - Not blocked
	order_id CHAR(4),
	FOREIGN KEY(cookie_name) REFERENCES Cookies(cookie_name),
	FOREIGN KEY(order_id) REFERENCES Orders(order_id)
);
	
DROP TABLE IF EXISTS Order_details;

CREATE TABLE Order_details(
    cookie_name TEXT,
    nbr_pallets INT,
    order_id CHAR(4),
    FOREIGN KEY(cookie_name) REFERENCES Cookies(cookie_name),
    FOREIGN KEY(order_id) REFERENCES Orders(order_id)
);

DROP TABLE IF EXISTS Customers;

CREATE TABLE Customers(
	customer_name	TEXT PRIMARY KEY,
	address			TEXT
);

DROP TABLE IF EXISTS Deliveries;

CREATE TABLE Deliveries(
	delivery_id		CHAR(4),
	order_id		CHAR(4),
	delivery_time	DATETIME,
	FOREIGN KEY(order_id) REFERENCES Orders(order_id)
);

DROP TABLE IF EXISTS Orders;

CREATE TABLE Orders(
	order_id		CHAR(4) PRIMARY KEY,
	customer_name	TEXT,
	order_status	INT, -- 1 - Delivered, 0 - Not delivered,
	FOREIGN KEY(customer_name) REFERENCES Customers(customer_name)
);

DROP TRIGGER IF EXISTS available_ingredients;

CREATE TRIGGER available_ingredients
    BEFORE INSERT ON Pallets
BEGIN
    SELECT CASE 
    WHEN EXISTS( SELECT cookie_name
            FROM Material_storage
            JOIN Cookie_ingredients
            USING (ingredient)
            WHERE cookie_name IS NEW.cookie_name AND amount*54 >= current_amount
    )
    THEN RAISE (ROLLBACK, "ERROR")
    END;
END; 

DROP TRIGGER IF EXISTS decrease_ingredient;

CREATE TRIGGER decrease_ingredient
    AFTER INSERT ON Pallets
BEGIN
    UPDATE Material_storage
    SET current_amount = current_amount -  (SELECT amount 
                                            FROM Cookie_ingredients
                                            WHERE cookie_name IS NEW.cookie_name AND ingredient IS Material_storage.ingredient 
                                            )*54
    WHERE ingredient IN    (SELECT ingredient 
                            FROM Cookie_ingredients
                            WHERE NEW.cookie_name IS cookie_name
                            )
    ;
END;


    
