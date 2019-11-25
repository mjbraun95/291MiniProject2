from bsddb3 import db
import re
import os

def b_terms():
    open("phase2output/te.idx", 'w').close()
    os.chdir("phase2output/")
    database = db.DB() #handle for Berkeley DB database
    DB_File = "terms.db"
    database.set_flags(db.DB_DUP)
    database.open(DB_File, None, db.DB_BTREE, db.DB_CREATE)
    curs = database.cursor()
    os.chdir("../phase2output/")
    open ('tempterms.txt', 'w').close()
    os.chdir("../phase1output/")
    os.system('sort terms.txt > ../phase2output/term.txt')
    os.chdir("../phase2output/")
    file = open("tempterms.txt", "a")
    with open('term.txt', 'r') as termfile:
        for line in termfile:
            line = line.strip()
            line = re.split("[-:]+", line)
            key = line[1]
            data = line[2]
            os.chdir("../phase2output/")
            file.write('%s\n%s\n' % (key, data))
    file.close()
    cwd = os.getcwd()
    print(cwd)
    curs = database.cursor()
    os.chdir("../phase2output/")
    os.system('db_load -f tempterms.txt -c duplicates=1 -T -t btree terms.db')
    os.remove("tempterms.txt")
    os.remove("term.txt")
    os.system('db_dump -p -f te.idx terms.db')
    result = 0
    os.chdir("../")
    curs.close()
    database.close()
    return result

if __name__ == "__main__":
    b_terms()