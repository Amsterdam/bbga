#!/bin/bash

set -e
set -u

# wait for database to load
source docker-wait.sh

echo 'unzipping latest bbga file'

unzip $(ls -Art data/*.zip | tail -n 1) -d /app/unzipped/

iconv -f WINDOWS-1251 -t UTF-8 -o metadata_utf8.csv metadata.csv


echo 'clear / build tables'
# clear and or create tables
python import_data.py --user $PARKEERVAKKEN_DB_USER \
		      --password $PARKEERVAKKEN_DB_PASSWORD \
		      --host $PARKEERVAKKEN_DB_PORT_5432_TCP_ADDR \
		      --port $PARKEERVAKKEN_DB_PORT_5432_TCP_PORT \
		      --database parkeervakken \
                      initialize

echo 'load parkeer data'
# run import / update data
python import_data.py --user $PARKEERVAKKEN_DB_USER \
		      --password $PARKEERVAKKEN_DB_PASSWORD \
		      --host $PARKEERVAKKEN_DB_PORT_5432_TCP_ADDR \
		      --port $PARKEERVAKKEN_DB_PORT_5432_TCP_PORT \
		      --database parkeervakken \
                      update \
                      --source /app/unzipped

echo 'parkeerdata DONE'
