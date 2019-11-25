from bsddb3 import db
import re
import os

def b_emails():
    open("phase2output/em.idx", 'w').close()
    database = db.DB() #handle for Berkeley DB database
    os.chdir("phase2output/")
    DB_File = "emails.db"
    database.open(DB_File, None, db.DB_BTREE, db.DB_CREATE)
    curs = database.cursor()
    os.chdir("../phase2output/")
    open ('tempemails.txt', 'w').close()
    os.chdir("../phase1output/")
    os.system('sort -u emails.txt > ../phase2output/email.txt')
    os.chdir("../phase2output/")
    file = open("tempemails.txt", "a")
    with open('email.txt', 'r') as emailfile:
        for line in emailfile:
            line = line.strip()
            print(line)
            line = re.split("[:]+", line)
            print(line)
            key = line[0]
            print(key)
            data = line[1]
            print(data)
            os.chdir("../phase2output/")
            file.write('%s\n%s\n' % (key, data))
    file.close()
    os.chdir("../phase2output/")
    os.system('db_load -f tempemails.txt -T -t btree emails.db')
    os.remove("tempemails.txt")
    os.remove("email.txt")
    os.system('db_dump -p -f em.idx emails.db')
    result = 0
    os.chdir("../")
    curs.close()
    database.close()
    return result

if __name__ == "__main__":
    b_emails()