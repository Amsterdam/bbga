
BBGA API
========


Requirements
------------

* Docker-Compose (required)


Developing
----------

Use `docker-compose` to start a local database.

	(sudo) docker-compose start

or

	docker-compose up


The API should now be available on http://localhost:8102/

The Database should now be available on 127.0.0.1:5406


Importing data
--------------

### variables

>   ./manage.py run_import /path/to/csv/bbga_tableau.csv

### metadata

>   ./manage.py run_import /path/to/csv/meta.csv bbga_data_meta
