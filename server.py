import os
from datetime import datetime
# import gurobipy as gp
import sqlite3
import logging
import json

halt = False
InputPath = "Input"
running = False

# input_list = os.listdir(InputPath)
# input_file = input_list[0]
# file_path = "gurobi_cl ResultFile=Output/"+input_file[:-3]+".sol Input/"+input_file
# os.system(file_path)

# read config file
# to do
cf = open('config.conf')
conf = cf.read()
cf_dict = json.loads(conf)

# try catch over while loop >> if error >> save status to db
# to do

# module signal >> try catch >> assign time limit when connect to db, update db
# to do 

# supervisor ctl
# to do

while not halt:
    # connect to database
    # try-catch open db >> if not success >> save log
    try:
        queue = sqlite3.connect('queue_server.db')
        cursor = queue.cursor()
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        # add error to 
    print("Connected successfully")


    # get table
    # get processing queue and pick first row
    queue_table = cursor.execute("SELECT FIRST(*) from QUEUE WHERE STATUS='processing'")

    queue_table = queue_table.fetchall()

    queue.commit()
    queue.close()
    # Check time    
    now = datetime.now()
    input_hour = now.hour
    # Kill process at 7.00 a.m.
    # to do

    if len(queue_table)>0:

        for row in queue_table:
            if row[2]=='processing':
                if row[1] == 'plant':
                    # update running status
                    # read input and save as .py
                    input_name = 'Input/'+str(row[0])+'.py'
                    f = open(input_name,'w')
                    f.write(row[3])
                    f.close()
                    print('read completely')
                    # solve problem
                    run_cmd = 'python3 '+input_name + " >> a.out"
                    os.system(run_cmd)
                    print('solve completely')
                    # update solution
                    output_path = 'Output/'+str(row[0])+'.sol'
                    o = open(output_path)
                    output = o.read()
                    o.close()
                    cursor.execute("UPDATE QUEUE SET STATUS = ?,OUTPUT = ? WHERE ID= ? ",('complete',output,row[0]))
                    queue.commit()
                    print('update completely')
                else :
                    if (input_hour <= 7) or (input_hour >= 17):
                        # read input and save as .py
                        input_name = 'Input/'+str(row[0])+'.py'
                        f = open(input_name,'w')
                        f.write(row[3])
                        f.close()
                        print('read completely')
                        # solve problem
                        run_cmd = 'python3 '+input_name
                        os.system(run_cmd)
                        print('solve completely')
                        # update solution
                        output_path = 'Output/'+str(row[0])+'.sol'
                        o = open(output_path)
                        output = o.read()
                        o.close()
                        cursor.execute("UPDATE QUEUE SET STATUS = ?,OUTPUT = ? WHERE ID= ? ",('complete',output,row[0]))
                        queue.commit()
                        print('update completely')
            # break
    

