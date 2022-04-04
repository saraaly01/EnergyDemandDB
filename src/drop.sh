#!/bin/bash

psql -U postgres -d EDG -c "DROP TABLE BUILDING;"
psql -U postgres -d EDG -c "DROP TABLE METER_ENTRY;"
psql -U postgres -d EDG -c "DROP TABLE WEATHER;"
psql -U postgres -d EDG -c "DROP TABLE METER;"

