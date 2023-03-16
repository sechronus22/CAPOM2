#!/usr/bin/python

import sqlite3
conn = sqlite3.connect('queue_server.db')

conn.execute('''CREATE TABLE QUEUE_TABLE
       (PROJECT_ID  VARCHAR(100) NOT NULL PRIMARY KEY,
       SENDER  VARCHAR(100)    NOT NULL,
       CCPS_VALID  VARCHAR(100) NOT NULL,
       STATUS  VARCHAR(100)     NOT NULL,
       INPUT  VARCHAR(50000)   NOT NULL,
       OUTPUT  VARCHAR(50000),
       LOG VARCHAR(50000));''')

conn.commit()
conn.close()

# field project_id

# add solver option VARCHAR 