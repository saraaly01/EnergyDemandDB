#!/bin/bash

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
Month varchar(9) PRIMARY KEY,
Avg_temp decimal(3,1)
);"

psql -U postgres -d EDG -c "CREATE TABLE METER_ENTRY(
meconsumpID char(10) PRIMARY KEY,
Start_date date,
End_date date,
Usage decimal(10,2),
Cost decimal(10,2),
mName varchar(4),
FOREIGN KEY (mName) REFERENCES meter (mName)
);"

psql -U postgres -d EDG -c "\\copy BUILDING FROM '$SCRIPT_DIR/build.csv' csv header"
psql -U postgres -d EDG -c "\\copy METER FROM '$SCRIPT_DIR/meter_data.csv' csv header"
psql -U postgres -d EDG -c "\\copy WEATHER FROM '$SCRIPT_DIR/degree_days.csv' csv header"
psql -U postgres -d EDG -c "\\copy METER_ENTRY FROM '$SCRIPT_DIR/mentries.csv' csv header"



