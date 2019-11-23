from bsddb3 import db
import re
import os
database = db.DB() #handle for Berkeley DB database
DB_File = "miniproject2.db"
database.open(DB_File, None, db.DB_BTREE, db.DB_CREATE)
curs = database.cursor()

def b_emails():
    open ('emails.txt', 'w').close()
    with open('emails.txt', 'r') as emailfile:
        for line in emailfile:
            line = line.strip()
            print(line)
            line = re.split("[:]+", line)
            print(line)
            key = line[0]
            print(key)
            data = line[1]
            print(data)
            #database.put(b'%s' % (key), data)
            file = open("tempemails.txt", "a")
            file.write('%s\n%s\n' % (key, data))
            file.close()

    os.chdir("C:\\Users\\Ishara\\OneDrive\\University of Alberta\\2019\\YEAR 2\\CMPUT 291\\mini project 2")
    os.system('db_load -f tempemails.txt -T -t btree miniproject2.db')
    os.remove("tempemails.txt")
    os.system('db_dump -p -f em.idx miniproject2.db')

    for key in database.keys():
        print('{}: {}'.format(key, database[key]))

    result = database.get(b'bcc-alb@cpuc.ca.gov')
    print(result)

    curs.close()
    database.close()

b_emails()