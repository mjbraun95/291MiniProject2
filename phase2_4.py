from bsddb3 import db
import re
import os

def b_dates():
    open("phase1output/da.idx", 'w').close()
    database = db.DB() #handle for Berkeley DB database
    os.chdir("phase2output/")
    DB_File = "dates.db"
    database.open(DB_File, None, db.DB_BTREE, db.DB_CREATE)
    curs = database.cursor()
    os.chdir("../phase2output/")
    open ('tempdates.txt', 'w').close()
    os.chdir("../phase1output/")
    os.system('sort -u dates.txt > ../phase2output/date.txt')
    os.chdir("../phase2output/")
    file = open("tempdates.txt", "a")
    with open('date.txt', 'r') as datesfile:
        for line in datesfile:
            line = line.strip()
            line = re.split("[:]+", line)
            key = line[0]
            data = line[1]
            os.chdir("../phase2output/")
            file.write('%s\n%s\n' % (key, data))
    file.close()

    os.chdir("../phase2output/")
    os.system('db_load -f tempdates.txt -T -t btree dates.db')
    os.remove("tempdates.txt")
    os.remove("date.txt")
    os.system('db_dump -p -f da.idx dates.db')
    result = 0
    print(result)
    os.chdir("../")

    curs.close()
    database.close()
    return result

if __name__ == "__main__":
    b_dates()