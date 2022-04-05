#!/bin/bash

#Date: 4/4/2022
#Written: Andrew Michael

#This script drops all the tables in the EDB database.

psql -U postgres -d EDG -c "DROP TABLE BUILDING;"
psql -U postgres -d EDG -c "DROP TABLE METER_ENTRY;"
psql -U postgres -d EDG -c "DROP TABLE WEATHER;"
psql -U postgres -d EDG -c "DROP TABLE METER;"

psql postgres -c "DROP DATABASE \"EDG\";"

