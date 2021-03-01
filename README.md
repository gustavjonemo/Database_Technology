# EDAF75, project report

This is the report for

 + Robin Vinterbladh, `ro3413vi-s`
 + Gustav Jönemo, `gu1673jo-s `
 + Rebecka Källén, `elt14lka`

We solved this project on our own, except for:

 + The Peer-review meeting
 + 


## ER-design

The model is in the file [`er-model.png`](er-model.png):

<center>
    <img src="er-model.png" width="100%">
</center>



## Relations

The ER-model above gives the following relations (neither
[Markdown](https://docs.gitlab.com/ee/user/markdown.html)
nor [HTML5](https://en.wikipedia.org/wiki/HTML5) handles
underlining withtout resorting to
[CSS](https://en.wikipedia.org/wiki/Cascading_Style_Sheets),
so we use bold face for primary keys, italicized face for
foreign keys, and bold italicized face for attributes which
are both primary keys and foreign keys):

+ material_delivery(**storage_id**, date, time, ingredient, amount)
+ material_storage(**ingredient**, grams, storage_id)
+ recipies(cookie_name, ingredient, grams)
+ amounts(**cookie_name**, nbr_bags, nbr_boxes)
+ pallets(**pallet_id**, cookie_name, date, time, delivery_status, blocked, order_id)
+ customers(**customer_name**, address)
+ orders(**order_id**, customer_name, nbr_pallets, cookie_name, order_status)
+ deliveries(delivety_id, order_id, date, time)


## Scripts to set up database

The scripts used to set up and populate the database are in:

 + [`create-schema.sql`](create-schema.sql) (defines the tables), and
 + [`initial-data.sql`](initial-data.sql) (inserts data).

So, to create and initialize the database, we run:

```shell
sqlite3 krusty-db.sqlite < create-schema.sql
sqlite3 krusty-db.sqlite < initial-data.sql
```

(or whatever you call your database file).

## How to compile and run the program

This section should give a few simple commands to type to
compile and run the program from the command line, such as:

```shell
./gradlew run
```

or, if you put your commands into a `Makefile`:

```shell
make compile
make run
```
