from bsddb3 import db
import re
import os

def b_emails():
    database = db.DB() #handle for Berkeley DB database
    os.chdir("phase2output/")
    DB_File = "miniproject2.db"
    database.open(DB_File, None, db.DB_BTREE, db.DB_CREATE)
    curs = database.cursor()
    os.chdir("../phase2output/")
    open ('tempemails.txt', 'w').close()
    os.chdir("../phase1output/")
    os.system('sort -u emails.txt > ../phase2output/email.txt')
    os.chdir("../phase2output/")
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
            #database.put(b'%s' % (key), data)
            os.chdir("../phase2output/")
            file = open("tempemails.txt", "a")
            file.write('%s\n%s\n' % (key, data))
            file.close()

    # input("Press enter to continue.")
    #os.chdir("C:\\Users\\Ishara\\OneDrive\\University of Alberta\\2019\\YEAR 2\\CMPUT 291\\mini project 2")
    os.chdir("../phase2output/")
    os.system('db_load -f tempemails.txt -T -t btree miniproject2.db')
    os.remove("tempemails.txt")
    os.remove("email.txt")
    os.system('db_dump -p -f em.idx miniproject2.db')

    for key in database.keys():
        print('{}: {}'.format(key, database[key]))

    result = database.get(b'bcc-alb@cpuc.ca.gov')
    print(result)
    os.chdir("../")

    curs.close()
    database.close()

if __name__ == "__main__":
    b_emails()