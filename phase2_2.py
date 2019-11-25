from bsddb3 import db
import re
import os

def b_terms():
    open("phase2output/te.idx", 'w').close()
    database = db.DB() #handle for Berkeley DB database
    os.chdir("phase2output/")
    DB_File = "terms.db"
    database.open(DB_File, None, db.DB_BTREE, db.DB_CREATE)
    curs = database.cursor()
    #os.chdir("C:\\Users\\Ishara\\OneDrive\\University of Alberta\\2019\\YEAR 2\\CMPUT 291\\mini project 2")
    #os.system('sort -u terms.txt > output.txt')
    #os.chdir("../phase1output/")
    os.chdir("../phase2output/")
    open ('tempterms.txt', 'w').close()
    os.chdir("../phase1output/")
    os.system('sort terms.txt > ../phase2output/term.txt')
    os.chdir("../phase2output/")
    with open('term.txt', 'r') as termfile:
        for line in termfile:
            line = line.strip()
            #print(line)
            line = re.split("[-:]+", line)
            #print(line)
            key = line[1]
            #print(key)
            data = line[2]
            #print(data)
            #database.put(b'%s' % (key), data)
            os.chdir("../phase2output/")
            file = open("tempterms.txt", "a")
            file.write('%s\n%s\n' % (key, data))
            file.close()
    cwd = os.getcwd()
    print(cwd)
    #os.chdir("/cshome/hettiara/Documents/291/291MiniProject2/phase1output/")
    curs = database.cursor()
    #os.chdir("../phase1output/")
    os.chdir("../phase2output/")
    os.system('db_load -f tempterms.txt -T -t btree terms.db')
    os.remove("tempterms.txt")
    os.remove("term.txt")
    #os.remove("output.txt")
    os.system('db_dump -p -f te.idx terms.db')

    try:
        for key in database.keys():
            print('{}: {}'.format(key, database[key]))
    except db.DBPageNotFoundError:
        os.chdir("../")
        b_terms()
        return
    result = database.get(b'dave')
    print(result)
    os.chdir("../")

    curs.close()
    database.close()

if __name__ == "__main__":
    b_terms()