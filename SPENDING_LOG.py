import sqlite3
import datetime
import os.path
import pickle


def make_file(conn):
    c = conn.cursor()
    c.execute('CREATE TABLE SpendingLog(ID, Date, Item, Price, Type)')
    conn.commit()
    c.close()


def insert_log(sqlid, date, item, price, itemtype):
    try:
        c = conn.cursor()
        print("Connection established.")
        insert_query = '''INSERT INTO SpendingLog 
                              (ID, Date, Item, Price, Type) 
                              VALUES
                              (?, ?, ?, ?, ?)'''
        data_tuple = (sqlid, date, item, price, itemtype)
        c.execute(insert_query, data_tuple)
        conn.commit()
        print("Record inserted successfully into SpendingLog table.")
        c.close()
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        conn.close()
        print("The SQL connection is now closed.")

#############################################################################

#connects and makes files if they don't exist
if os.path.isfile('./SpendingLog.db') is False:
    conn = sqlite3.connect('SpendingLog.db')
    make_file(conn)
    typeDict = {}
    with open('saved_id.txt', 'w') as i:
        i.write('1')
        i.close()
    with open('saved_dict.txt', 'wb') as d:
        pickle.dump(typeDict, d)
        d.close()
else:
    conn = sqlite3.connect('SpendingLog.db')
#writing index number
with open('saved_id.txt', 'r') as i:
    indexNum = i.readline()
    indexNum = int(indexNum)
    indexNum += 1
    i.close()
    with open('saved_id.txt', 'w') as i:
        i.write(str(indexNum))
        i.close()
#collecting item
print('What did you buy?')
logItem = input()
#collecting cost
print('How much did it cost?')
logPrice = input()
if '.' not in logPrice:
    logPrice = float(logPrice + '.00')
#collecting type
with open('saved_dict.txt', 'rb') as d:
    typeDict = pickle.load(d)
    if logItem not in typeDict:
        print('What kind of purchase was it?')
        logType = input().title()
        typeDict.update({logItem : logType})
        with open('saved_dict.txt', 'wb') as d:
            pickle.dump(typeDict, d)
            d.close()
    else:
        logType = typeDict[logItem]
#today's date
theDate = datetime.date.today()

insert_log(indexNum, theDate, logItem, logPrice, logType)
