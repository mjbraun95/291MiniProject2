####text = ''
    #if event == 'start':
        #print ('<%s>' % elem.tag, end = '')
        #if elem.text != None:
        #    text = elem.text.strip()
        #if text != '':
         #   print(text, end='')
    #elif event == 'end':
     #   print()
      #  elem.clear()
        #print ('<%s>' % elem.tag)
        #print('here')

from xml.etree import ElementTree
import re
xml_iter = ElementTree.iterparse('emails.xml', events = ('start','end'))

def create_terms():

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
                            #print('write into file: s-%s:%s' % (term, rowid))
                            file = open("terms.txt", "a")
                            file.write('s-%s:%s\n' % (term, rowid))
                            file.close()
                        elif elem.tag == 'body'and len(term) > 2:
                            #print('write into file: b-%s:%s' % (term, rowid))
                            file = open("terms.txt", "a")
                            file.write('b-%s:%s\n' % (term, rowid))
                            file.close()
        elif event == 'end':
            print(end='')
            elem.clear()

def create_emails():
    for event, elem in xml_iter:
        text = ''
        if event == 'start':
            if elem.tag == 'row':
                rowid = elem.text
            if elem.tag == 'from' or elem.tag == 'to' or elem.tag == 'cc' or elem.tag == 'bcc':
                if elem.text != None:
                    text = elem.text
                    if elem.tag == 'from':
                        file = open("emails.txt", "a")
                        file.write('from-%s:%s\n' % (text, rowid))
                        file.close()
                        #print('write into file: from-%s:%s' % (text, rowid))
                    elif elem.tag == 'to':
                        file = open("emails.txt", "a")
                        file.write('to-%s:%s\n' % (text, rowid))
                        file.close()
                        #print('write into file: to-%s:%s' % (text, rowid))
                    if elem.tag == 'cc':
                        file = open("emails.txt", "a")
                        file.write('cc-%s:%s\n' % (text, rowid))
                        file.close()
                        #print('write into file: cc-%s:%s' % (text, rowid))
                    elif elem.tag == 'bcc':
                        file = open("emails.txt", "a")
                        file.write('bcc-%s:%s\n' % (text, rowid))
                        file.close()
                        #print('write into file: bcc-%s:%s' % (text, rowid))
        elif event == 'end':
            print(end='')
            elem.clear()

def create_dates():
    for event, elem in xml_iter:
        text = ''
        if event == 'start':
            if elem.tag == 'row':
                rowid = elem.text
            if elem.tag == 'date':
                date = elem.text
                file = open("dates.txt", "a")
                file.write('%s:%s\n' % (date, rowid))
                file.close()
                #print('write into file: %s:%s' % (date, rowid))
        elif event == 'end':
            elem.clear()

def get_rowid(elem):
    row = elem.find('row')
    if row != None:
        id = row.text
        file = open("recs.txt", "a")
        file.write(id)
        #file.write('<%s>' % elem.tag)
        file.close()

def create_recs():
    for event, elem in xml_iter:
        if event == 'start':
            if elem.tag == 'mail':
                row = elem.find('row')
                if row != None:
                    id = row.text
                    file = open("recs.txt", "a")
                    file.write(id)
                    file.close()

                text = ElementTree.tostring(elem, short_empty_elements=False)

                text = text.decode("utf-8")
                text = text.replace('\n', '&#10;')
                file = open("recs.txt", "a")
                file.write(text)
                file.close()
        elif event == 'end':
            if elem.tag ==('mail'):
                file = open("recs.txt", "a")
                file.write('</%s>' % elem.tag)
                file.write('\n')
                file.close()
            #elem.clear()

#create_terms()
#create_emails()
#create_dates()
#create_recs()