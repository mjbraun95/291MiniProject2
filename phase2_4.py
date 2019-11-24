from bsddb3 import db
import re
import os

def b_dates():
    open("phase1output/da.idx", 'w').close()
    database = db.DB() #handle for Berkeley DB database
    os.chdir("phase2output/")
    DB_File = "dastes.db"
    database.open(DB_File, None, db.DB_BTREE, db.DB_CREATE)
    curs = database.cursor()
    os.chdir("../phase2output/")
    open ('tempdates.txt', 'w').close()
    os.chdir("../phase1output/")
    os.system('sort -u dates.txt > ../phase2output/date.txt')
    os.chdir("../phase2output/")
    #os.system('sort dates.txt > dates.txt')
    with open('date.txt', 'r') as datesfile:
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
            file = open("tempdates.txt", "a")
            #print(key)
            file.write('%s\n%s\n' % (key, data))
            file.close()

    os.chdir("../phase2output/")
    os.system('db_load -f tempdates.txt -T -t btree dates.db')
    os.remove("tempdates.txt")
    os.remove("date.txt")
    #os.remove("dates.txt")
    os.system('db_dump -p -f da.idx dates.db')

    for key in database.keys():
        print('{}: {}'.format(key, database[key]))

    result = database.get(b'2000/10/05')
    print(result)
    os.chdir("../")

    curs.close()
    database.close()

if __name__ == "__main__":
    b_dates()