import os
from datetime import datetime
# import gurobipy as gp
import sqlite3
import logging
import json
import pandas as pd

halt = False
InputPath = "Input"
running = False

# read config file
# to do
with open('config.conf') as config_file:
    conf = json.load(config_file)

queue_db_name = conf['DATABASE_NAME']
queue_table_name = conf['QUEUE_TABLE_NAME']
queue_status_table = 'QUEUE_STATUS'
table_field_list= conf['FIELD_MAP'][0]
input_dir = conf['INPUT_PATH']
output_dir = conf['OUTPUT_PATH']

# try catch over while loop >> if error >> save status to db
# to do

# module signal >> try catch >> assign time limit when connect to db, update db
# to do 

# supervisor ctl
# to do

while not halt:

    # Check time    
    now = datetime.now()
    cur_hour = now.hour
    cur_minute = now.minute

    # Kill process at 7.00 a.m.
    # to do 

    # solve models at 7.00 a.m.
    if cur_hour == 7 and cur_minute == 0 :
        try :
            queue_db = sqlite3.connect(queue_db_name)
        except Exception as e:
            print(e)

        # print("Database connected successfully")

        # get table
        # get processing queue which CCPS_VALID == 'TRUE'

        else :
            cursor = queue_db.cursor()
            queue_table = cursor.execute("SELECT * from "+ queue_table_name + " WHERE STATUS =='processing' and CCPS_VALID == 'TRUE' ")
            queue_table = queue_table.fetchall()

            queue_db.commit()
            queue_db.close()

            #solve each model
            
            for row in queue_table:

                # read input and save as .py
                input_path = input_dir+str(row[0])+'.py'
                f = open(input_path,'w')
                f.write(row[4])
                f.close()
                print('Read completely')

                # solve problem
                run_cmd = 'python3 '+input_path + " >> "+output_dir + str(row[0])+ ".out"
                try:
                    os.system(run_cmd)
                except Exception as e:
                    # save log if error
                    queue_db = sqlite3.connect(queue_db_name)
                    cursor = queue_db.cursor()
                    cursor.execute("UPDATE "+queue_table_name+ " SET STATUS = ? and LOG = ? WHERE PROJECT_ID == ? ",('failed',e,row[0]))
                    queue_db.commit() 
                    queue_db.close()
                else :
                    print('Solve completely')

                    # update solution and status
                    output_path = output_dir + str(row[0])+'.out'
                    o = open(output_path)
                    output = o.read()
                    o.close()

                    queue_db = sqlite3.connect(queue_db_name)
                    cursor = queue_db.cursor()
                    cursor.execute("UPDATE " + queue_table_name + " SET STATUS = ?,OUTPUT = ? WHERE PROJECT_ID == ? ",('complete',output,row[0]))
                    queue_db.commit()
                    queue_db.close()
                    print('Update completely')

                    # delete input and output file
                    os.remove(input_path)
                    os.remove(output_path)

    # connect to database
    # try-catch open db >> if not success >> save log
    try :
        queue_db = sqlite3.connect(queue_db_name)
    except:
        print('Queue server database opening error')

    # print("Database connected successfully")

    # get table
    # get processing queue and pick first row
    cursor = queue_db.cursor()
    queue_table = cursor.execute("SELECT * from "+ queue_table_name + " WHERE STATUS =='processing' and CCPS_VALID == 'FALSE' ")
    queue_table = queue_table.fetchall()

    queue_db.commit()
    queue_db.close()

    if len(queue_table)>0:

        for row in queue_table:
            # check whether model is from CCPS or not
            if row[1] == 'CCPS':
                # read input and save as .py
                input_path = input_dir+str(row[0])+'.py'
                f = open(input_path,'w')
                f.write(row[4])
                f.close()
                print('Read completely')

                # solve problem
                run_cmd = 'python3 '+input_path + " >> "+output_dir + str(row[0])+ ".out"
                try:
                    os.system(run_cmd)
                except Exception as e:
                    # save log if error
                    queue_db = sqlite3.connect(queue_db_name)
                    cursor = queue_db.cursor()
                    cursor.execute("UPDATE "+queue_table_name+ " SET STATUS = ? and LOG = ? WHERE PROJECT_ID == ? ",('failed',e,row[0]))
                    queue_db.commit() 
                    queue_db.close()
                else :
                    print('Solve completely')

                    # update solution and status
                    output_path = output_dir + str(row[0])+'.out'
                    o = open(output_path)
                    output = o.read()
                    o.close()

                    queue_db = sqlite3.connect(queue_db_name)
                    cursor = queue_db.cursor()
                    cursor.execute("UPDATE " + queue_table_name + " SET STATUS = ?,OUTPUT = ? WHERE PROJECT_ID == ? ",('complete',output,row[0]))
                    queue_db.commit()
                    queue_db.close()
                    print('Update completely')

                    # delete input and output file
                    os.remove(input_path)
                    os.remove(output_path)

                break

            else :
                # non factory model cannot be solved between 7.00 a.m. and 5.00 p.m.
                if (cur_hour <= 7) or (cur_hour >= 17):
                    # read input and save as .py

                    input_path = input_dir+str(row[0])+'.py'
                    f = open(input_path,'w')
                    f.write(row[4])
                    f.close()
                    print('Read completely')

                    # solve problem
                    run_cmd = 'python3 '+input_path + " >> "+output_dir + str(row[0])+ ".out"
                    try:
                        os.system(run_cmd)
                    except Exception as e:
                        # save log if error
                        queue_db = sqlite3.connect(queue_db_name)
                        cursor = queue_db.cursor()
                        cursor.execute("UPDATE "+queue_table_name+ " SET STATUS = ? and LOG = ? WHERE PROJECT_ID == ? ",('failed',e,row[0]))
                        queue_db.commit() 
                        queue_db.close()
                    else :
                        print('Solve completely')

                        # update solution and status
                        output_path = output_dir + str(row[0])+'.out'
                        o = open(output_path)
                        output = o.read()
                        o.close()

                        queue_db = sqlite3.connect(queue_db_name)
                        cursor = queue_db.cursor()
                        cursor.execute("UPDATE " + queue_table_name + " SET STATUS = ?,OUTPUT = ? WHERE PROJECT_ID == ? ",('complete',output,row[0]))
                        queue_db.commit()
                        queue_db.close()
                        print('Update completely')

                        # delete input and output file
                        os.remove(input_path)
                        os.remove(output_path)

                break
    

