from bsddb3 import db
import re
import os
database = db.DB() #handle for Berkeley DB database
DB_File = "miniproject2.db"
database.open(DB_File, None, db.DB_BTREE, db.DB_CREATE)
curs = database.cursor()

def b_dates():

    with open("phase2input/dates.txt", "r") as datesfile:
        for line in datesfile:
            line = line.strip()
            #if char in line() !='\n':
            #print(line)
            line = re.split("[:]+", line)
            #print(line)
            key = line[0].encode()
            #print(key)
            data = line[1]
            #print(data)
            #database.put(b'%s' % (key), data)
            file = open("tempdates.txt", "a")
            print(key)
            file.write('%s\n%s\n' % (key, data))
            file.close()

    os.chdir("C:\\Users\\Ishara\\OneDrive\\University of Alberta\\2019\\YEAR 2\\CMPUT 291\\mini project 2")
    os.system('db_load -f tempdates.txt -T -t btree miniproject2.db')
    #os.remove("tempdates.txt")
    os.system('db_dump -p miniproject2.db')

    result = database.get(b'2000/09/05')
    print(result)

    #curs.close()
    #database.close()

b_dates()