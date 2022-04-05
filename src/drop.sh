#!/bin/bash

#Created on 4/4/2022 by A.M

#Drops tables in the database

psql -U postgres -d EDG -c "DROP TABLE BUILDING;"
psql -U postgres -d EDG -c "DROP TABLE METER_ENTRY;"
psql -U postgres -d EDG -c "DROP TABLE WEATHER;"
psql -U postgres -d EDG -c "DROP TABLE METER;"

psql postgres -c "DROP DATABASE \"EDG\";"

