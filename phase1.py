from xml.etree import cElementTree
import re


def create_terms(xmlInput):
    xml_iter = cElementTree.iterparse(xmlInput, events = ('start','end'))
    open("phase1output/terms.txt", 'w').close()
    file = open("phase1output/terms.txt", "a")
    for event, elem in xml_iter:
        text = ''
        if event == 'start':
            if elem.tag == 'row':
                rowid = elem.text
            if elem.tag == 'subj' or elem.tag == 'body':
                if elem.text != None:
                    text = elem.text.strip()
                    text = text.split()
                    i = 0
                    while i < len(text):
                        term = text[i]
                        cleanString = re.sub('[^A-Za-z0-9]+', '',term.lower())
                        text[i] = cleanString
                        i += 1
                    for term in text:
                        if elem.tag == 'subj' and len(term) > 2:
                            file.write('s-%s:%s\n' % (term, rowid))
                        elif elem.tag == 'body'and len(term) > 2:
                            file.write('b-%s:%s\n' % (term, rowid))
        elif event == 'end':
            print(end='')
            elem.clear()
    file.close()

def create_emails(xmlInput):
    xml_iter = cElementTree.iterparse(xmlInput, events = ('start','end'))
    open("phase1output/emails.txt", 'w').close()
    file = open("phase1output/emails.txt", "a")
    for event, elem in xml_iter:
        text = ''
        if event == 'start':
            if elem.tag == 'row':
                rowid = elem.text
            if elem.tag == 'from' or elem.tag == 'to' or elem.tag == 'cc' or elem.tag == 'bcc':
                if elem.text != None:
                    text = elem.text
                    if elem.tag == 'from':
                        file.write('from-%s:%s\n' % (text, rowid))
                    elif elem.tag == 'to':
                        file.write('to-%s:%s\n' % (text, rowid))
                    if elem.tag == 'cc':
                        file.write('cc-%s:%s\n' % (text, rowid))
                    elif elem.tag == 'bcc':
                        file.write('bcc-%s:%s\n' % (text, rowid))
        elif event == 'end':
            print(end='')
            elem.clear()
    file.close()

def create_dates(xmlInput):
    xml_iter = cElementTree.iterparse(xmlInput, events = ('start','end'))
    open("phase1output/dates.txt", 'w').close()
    file = open("phase1output/dates.txt", "a")
    for event, elem in xml_iter:
        text = ''
        if event == 'start':
            if elem.tag == 'row':
                rowid = elem.text
            if elem.tag == 'date':
                date = elem.text
                file.write('%s:%s\n' % (date, rowid))
        elif event == 'end':
            elem.clear()
    file.close()

def create_recs(xmlInput):
    xml_iter = cElementTree.iterparse(xmlInput, events = ('start','end'))
    open("phase1output/recs.txt", 'w').close()
    file = open("phase1output/recs.txt", "a")
    for event, elem in xml_iter:
        if event == 'start':
            if elem.tag == 'mail':
                row = elem.find('row')
                if row != None:
                    id = row.text
                    if id != None:
                        file.write(id)
                text = cElementTree.tostring(elem, short_empty_elements=False)
                text = text.decode("utf-8")
                text = text.replace('\n', '&#10;')
                file.write(text)
        elif event == 'end':
            if elem.tag ==('mail'):
                file.write('</%s>' % elem.tag)
                file.write('\n')
    file.close()

if __name__ == "__main__":
    xmlInput = input("Name of xml file (default= '1k.xml'): ")
    if xmlInput == "":
        xmlInput = "1k.xml"
    ct = input("Create terms? (Y/n)")
    ce = input("Create emails? (Y/n)")
    cd = input("Create dates? (Y/n)")
    cr = input("Create recs? (Y/n)")
    if ct != "n" and ct != "N":
        print("Creating terms...", end="")
        create_terms(xmlInput)
        print("Done!")
    if ce != "n" and ce != "N":
        print("Creating emails...", end="")
        create_emails(xmlInput)
        print("Done!")
    if cd != "n" and cd != "N":
        print("Creating dates...", end="")
        create_dates(xmlInput)
        print("Done!")
    if cr != "n" and cr != "N":
        print("Creating recs...", end="")
        create_recs(xmlInput)
        print("Done!")