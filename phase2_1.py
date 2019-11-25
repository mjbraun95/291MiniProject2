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
    # a hash index on recs.txt with row ids as keys and the full email record as data,
    os.chdir("../phase2output/")
    open ('temprecs.txt', 'w').close()
    os.chdir("../phase1output/")
    os.system('sort -u recs.txt > ../phase2output/rec.txt')
    os.chdir("../phase2output/")
    file = open("temprecs.txt", "a")
    with open('rec.txt', 'r') as recfile:
        #id = recfile.read(1).encode()
        for line in recfile:
            key = ''
            for char in line:
                if char != '<':
                    key +=char
                else:
                    break
            start = len(key)
            #print(key)
            data = line[start:]
            #print(data)
            #data= data.replace('/', '')
            #database.put(b'%s' % (key.encode()), data)
            os.chdir("../phase2output/")
            file.write('%s\n%s' % (key, data))
    file.close()

    os.chdir("../phase2output/")
    #os.system('qwx')
    os.system('db_load -f temprecs.txt -T -t hash recs.db')
    os.remove("temprecs.txt")
    os.remove("rec.txt")
    os.system('db_dump -p -f re.idx recs.db')
    # try:
    #     for key in database.keys():
    #         print('{}: {}'.format(key, database[key]))
    # except db.DBPageNotFoundError:
    #     os.chdir("../")
    #     hash_recs()
    #     return
    result = database.get(b'1')
    # print(result)
    os.chdir("../")

    curs.close()
    database.close()
    
    return result

if __name__ == "__main__":
	hash_recs()