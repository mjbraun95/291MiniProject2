from bsddb3 import db
import re
import os
database = db.DB() #handle for Berkeley DB database
os.chdir("phase2output/")
DB_File = "miniproject2.db"
database.open(DB_File, None, db.DB_BTREE, db.DB_CREATE)
curs = database.cursor()

def b_dates():
    os.chdir("../phase2output/")
    open ('tempdate.txt', 'w').close()
    os.chdir("../phase1output/")
    #os.system('sort dates.txt > date.txt')
    with open('dates.txt', 'r') as datesfile:
        for line in datesfile:
            line = line.strip()
            #if char in line() !='\n':
            #print(line)
            line = re.split("[:]+", line)
            #print(line)
            key = line[0]
            #print(key)
            data = line[1]
            #print(data)
            #database.put(b'%s' % (key), data)
            os.chdir("../phase2output/")
            file = open("tempdate.txt", "a")
            #print(key)
            file.write('%s\n%s\n' % (key, data))
            file.close()

    os.chdir("../phase2output/")
    os.system('db_load -f tempdate.txt -T -t btree miniproject2.db')
    os.remove("tempdate.txt")
    #os.remove("date.txt")
    os.system('db_dump -p -f da.idx miniproject2.db')

    for key in database.keys():
        print('{}: {}'.format(key, database[key]))

    result = database.get(b'2000/10/05')
    print(result)

    curs.close()
    database.close()

b_dates()