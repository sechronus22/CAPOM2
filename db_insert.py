#!/usr/bin/python

import sqlite3
conn = sqlite3.connect('queue_server.db')
print("เปิดฐานข้อมูลสำเร็จ")
f = open('lp1.txt')
content = f.read()
f.close()

conn.execute("INSERT INTO QUEUE_TABLE VALUES (?, ?, ?, ?, ?, ?, ?)",('22','CCPS','TRUE','processing',content, None, None))
conn.commit()
conn.close()

# field project_id