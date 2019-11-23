from bsddb3 import db
import re
import os
database = db.DB() #handle for Berkeley DB database
DB_File = "miniproject2.db"
database.open(DB_File ,None, db.DB_HASH, db.DB_CREATE)
#database.open(DB_File ,None, DB_BTREE, db.DB_CREATE)
curs = database.cursor()

def hash_rec():
    # a hash index on recs.txt with row ids as keys and the full email record as data,
    os.chdir("../phase1output/")
    open ('temprecs.txt', 'w').close()
    with open('recs.txt', 'r') as recfile:
        #id = recfile.read(1).encode()
        for line in recfile:
            key = ''
            for char in line:
                if char != '<':
                    key +=char
                else:
                    break
            start = len(key)
            print(key)
            data = line[start:]
            print(data)
            #data= data.replace('/', '')
            #database.put(b'%s' % (key.encode()), data)
            file = open("temprec.txt", "a")
            file.write('%s\n%s' % (key, data))
            file.close()

    #os.chdir("C:\\Users\\Ishara\\OneDrive\\University of Alberta\\2019\\YEAR 2\\CMPUT 291\\mini project 2")
    os.system('db_load -f temprec.txt -T -t hash miniproject2.db')
    #os.remove("temprec.txt")
    #os.system('db_dump -p -f re.idx miniproject2.db')

    for key in database.keys():
        print('{}: {}'.format(key, database[key]))

    result = database.get(b'5')
    print(result)

    curs.close()
    database.close()

hash_rec()