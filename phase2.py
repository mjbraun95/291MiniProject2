import phase2_1, phase2_2, phase2_3, phase2_4

if __name__ == "__main__":
    p21 = input("Load recs.txt? (Y/n)")
    p22 = input("Load terms.txt? (Y/n)")
    p23 = input("Load emails.txt? (Y/n)")
    p24 = input("Load dates.txt? (Y/n)")

    if p21 != "n" and p21 != "N":
        print("Parsing recs.txt...", end="")
        phase2_1.hash_recs()
        print("Done!")
    if p22 != "n" and p22 != "N":
        print("Parsing terms.txt...", end="")
        phase2_2.b_terms()
        print("Done!")
    if p23 != "n" and p23 != "N":
        print("Parsing emails.txt...", end="")
        phase2_3.b_emails()
        print("Done!")
    if p24 != "n" and p24 != "N":
        print("Parsing dates.txt...", end="")
        phase2_4.b_dates()
        print("Done!")