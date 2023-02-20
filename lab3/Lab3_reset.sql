DROP TABLE IF EXISTS theaters;

CREATE TABLE theaters(
	t_name TEXT PRIMARY KEY,
	capacity INT
);

DROP TABLE IF EXISTS movies;

CREATE TABLE movies(
	imdb_key CHAR(9) PRIMARY KEY,
	title TEXT,
	year INT,
	duration INT
);

DROP TABLE IF EXISTS customers;

CREATE TABLE customers(
	username TEXT PRIMARY KEY,
	name TEXT,
	password TEXT
);


DROP TABLE IF EXISTS screenings;

CREATE TABLE screenings(
	screen_id TEXT DEFAULT (lower(hex(randomblob(16)))),
	seats INT,
	t_name TEXT,
	imdb_key CHAR(9),
	date DATE,
	start TIME,
	PRIMARY KEY (screen_id),
	FOREIGN KEY (t_name) REFERENCES theaters(t_name),
	FOREIGN KEY (imdb_key) REFERENCES movies(imdb_key)
);

DROP TABLE IF EXISTS tickets;

CREATE TABLE tickets(
	ticket_id TEXT DEFAULT (lower(hex(randomblob(16)))),
	username TEXT,
	screen_id TEXT,
	PRIMARY KEY (ticket_id),
	FOREIGN KEY (username) REFERENCES customers(username),
	FOREIGN KEY (screen_id) REFERENCES screenings(screen_id)
);



INSERT
INTO theaters(t_name, capacity)
VALUES	('Kino', 10),
		('Regal', 16),
		('Skandia', 100);