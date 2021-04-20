DROP TABLE IF EXISTS Cookie_ingredients;

CREATE TABLE Cookie_ingredients(
	cookie_name TEXT,
    ingredient  TEXT,
    amount      INT
);

DROP TABLE IF EXISTS Material_storage;

CREATE TABLE Material_storage(
	ingredient      TEXT PRIMARY KEY,
    current_amount  INT,
    date            DATE,
    time            TIME,
    last_deposit    INT
);

DROP TABLE IF EXISTS Cookie;

CREATE TABLE Cookie(
	cookie_name     TEXT PRIMARY KEY
);

DROP TABLE IF EXISTS Pallets;

CREATE TABLE Pallets(
	pallet_id CHAR(4) PRIMARY KEY,
	cookie_name TEXT,
	date DATE,
	time TIME,
	delivery_status INT,  -- 1 - Delivered, 0 - Not delivered
	blocked INT,        -- 1 - Blocked, 0 - Not blocked
	order_id CHAR(4)
);
	
DROP TABLE IF EXISTS Order_details;

CREATE TABLE Order_details(
    cookie_name TEXT,
    nbr_pallets INT,
    order_id CHAR(4)
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
	date			DATE,
	time			TIME
);

DROP TABLE IF EXISTS Orders;

CREATE TABLE Orders(
	order_id		CHAR(4) PRIMARY KEY,
	customer_name	TEXT,
	order_status	INT -- 1 - Delivered, 0 - Not delivered
);