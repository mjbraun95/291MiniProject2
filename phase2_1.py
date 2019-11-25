from bsddb3 import db
import re
import os

def hash_recs():
    open("phase2output/re.idx", 'w').close()
    database = db.DB() #handle for Berkeley DB database
    os.chdir("phase2output/")
    DB_File = "recs.db"
    database.open(DB_File, None, db.DB_HASH, db.DB_CREATE)
    curs = database.cursor()
    os.chdir("../phase2output/")
    open ('temprecs.txt', 'w').close()
    os.chdir("../phase1output/")
    os.system('sort -u recs.txt > ../phase2output/rec.txt')
    os.chdir("../phase2output/")
    file = open("temprecs.txt", "a")
    with open('rec.txt', 'r') as recfile:
        for line in recfile:
            key = ''
            for char in line:
                if char != '<':
                    key +=char
                else:
                    break
            start = len(key)
            data = line[start:]
            os.chdir("../phase2output/")
            file.write('%s\n%s' % (key, data))
    file.close()
    os.chdir("../phase2output/")
    os.system('db_load -f temprecs.txt -T -t hash recs.db')
    os.remove("temprecs.txt")
    os.remove("rec.txt")
    os.system('db_dump -p -f re.idx recs.db')
    result = 0
    os.chdir("../")
    curs.close()
    database.close()
    return result

if __name__ == "__main__":
	hash_recs()