
BBGA API
========

"Basis Bestand Getallen Amsterdam"

Requirements
------------

* Docker-Compose (required)


Developing
----------

Use `docker-compose` to start a local database.

	(sudo) docker-compose start

or

	docker-compose up


The API should now be available on http://localhost:8000/

The Database should now be available on 127.0.0.1:5406


Importing data
--------------


####

>   docker-compose run bbga ./manage.py migrate

>   docker-compose run bbga bash import_data.sh


### variables

>   ./manage.py run_import /path/to/csv/bbga_tableau.csv

### metadata

>   ./manage.py run_import /path/to/csv/meta.csv bbga_data_meta
