#!/bin/bash

#Last updated on 4/5/2022 1:10PM by K.K 

#This code will initialize the database "EDG" and populate it with the following data
#located in the following csv flies: build.csv, degree_days.csv, meter_data.csv, mentries.csv


SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

createdb EDG;

psql -U postgres -d EDG -c "CREATE TABLE BUILDING (
name text unique,
bID char(7) PRIMARY KEY,
Year_built char(4),
Prim_use text,
Eff_factor decimal(20,20),
Size integer);" 

psql -U postgres -d EDG -c "CREATE TABLE METER(
    mID char(8) PRIMARY KEY,
    mName varchar(4) UNIQUE,
    etype text,
    utype  text

);"

psql -U postgres -d EDG -c "CREATE TABLE WEATHER(
Month integer PRIMARY KEY,
Avg_temp decimal(3,1)
);"

psql -U postgres -d EDG -c "CREATE TABLE METER_ENTRY(
meconsumpID char(10) PRIMARY KEY,
Start_date date,
End_date date,
Usage decimal(10,2),
Cost decimal(10,2),
mName varchar(4),
mID char(10),
FOREIGN KEY (mID) REFERENCES meter (mID)
);"

psql -U postgres -d EDG -c "\\copy BUILDING FROM '$SCRIPT_DIR/build.csv' csv header"
psql -U postgres -d EDG -c "\\copy METER FROM '$SCRIPT_DIR/meter_data.csv' csv header"
psql -U postgres -d EDG -c "\\copy WEATHER FROM '$SCRIPT_DIR/degree_days.csv' csv header"
psql -U postgres -d EDG -c "\\copy METER_ENTRY FROM '$SCRIPT_DIR/mentries.csv' csv header"

printf "Table Names Created: \n BUILDING \n METER \n WEATHER \n METER_ENTRY\n"

