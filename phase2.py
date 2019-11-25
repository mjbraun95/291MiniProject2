import phase2_1, phase2_2, phase2_3, phase2_4
from bsddb3 import db
import os
import shutil

def initDB(DB_File):
    open("phase2output/re.idx", 'w').close()
    database = db.DB() #handle for Berkeley DB database
    os.chdir("phase2output/")
    
    database.open(DB_File, None, db.DB_HASH, db.DB_CREATE)
    os.chdir("../")
    database.close

if __name__ == "__main__":
    shutil.rmtree("phase2output")
    os.mkdir("phase2output")
    # os.chdir("phase2output")
    # os.remove("dates.db")
    # os.remove("emails.db")
    # os.remove("recs.db")
    # os.remove("terms.db")
    # os.remove("da.idx")
    # os.remove("em.idx")
    # os.remove("re.idx")
    # os.remove("te.idx")
    # os.chdir("../")
    p21 = input("Load recs.txt? (Y/n)")
    p22 = input("Load terms.txt? (Y/n)")
    p23 = input("Load emails.txt? (Y/n)")
    p24 = input("Load dates.txt? (Y/n)")

    if p21 != "n" and p21 != "N":
        # initDB("recs.db")
        print("Parsing recs.txt...", end="")
        phase2_1.hash_recs()
        print("Done!")
    if p22 != "n" and p22 != "N":
        # initDB("terms.db")
        print("Parsing terms.txt...", end="")
        phase2_2.b_terms()
        print("Done!")
    if p23 != "n" and p23 != "N":
        # initDB("emails.db")
        print("Parsing emails.txt...", end="")
        phase2_3.b_emails()
        print("Done!")
    if p24 != "n" and p24 != "N":
        # initDB("dates.db")
        print("Parsing dates.txt...", end="")
        phase2_4.b_dates()
        print("Done!")