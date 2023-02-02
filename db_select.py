import sqlite3
import pandas as pd

db = sqlite3.connect('queue_server.db')
cursor = db.cursor()

table_name = 'QUEUE_TABLE'

queue_table = cursor.execute("SELECT * from "+ table_name)
queue_table = queue_table.fetchall()

db.commit()
db.close()

for row in queue_table:
    print('Project ID:',row[0])
    print('Sender:',row[1])
    print('STATUS',row[3],'\n')
