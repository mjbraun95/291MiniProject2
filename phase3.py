from bsddb3 import db
import bsddb3
import re
import os

def parseRecord(record,lookIn,lookFor):
    startStr = "<{}>".format(lookIn)
    start = record.find(startStr) + len(startStr)
    endStr = "</{}>".format(lookIn)
    end = record.find(endStr)
    if record[start:end].lower().find(lookFor) != -1:
        return True
    else:
        return False

def parseregexRecord(record,lookIn,lookFor):
    startStr = "<{}>".format(lookIn)
    start = record.find(startStr) + len(startStr)
    endStr = "</{}>".format(lookIn)
    end = record.find(endStr)
    p = re.compile(lookFor + "*")
    if p.match(record[start:end].lower()) != None:
        return True
    else:
        return False

def parseidx(key, idxFile):
    idxOpen = open('phase2output/{}'.format(idxFile), 'r')
    valueArray = []
    for lineIndex, line in enumerate(idxOpen):
        if line[0] != " ":
            continue
        else:
            value = next(idxOpen)[1:-1]
            if line[1:-1].lower() == key and (value not in valueArray):
                valueArray.append(value)
    return valueArray

def parseregexidx(key, idxFile):
    idxOpen = open('phase2output/{}'.format(idxFile), 'r')
    valueArray = []
    p = re.compile(key + "*")
    for lineIndex, line in enumerate(idxOpen):
        if line[0] != " ":
            continue
        else:
            value = next(idxOpen)[1:-1]
            if p.match(line[1:-1].lower()) != None and (value not in valueArray):
                valueArray.append(value)
    return valueArray

def parsedateidx(key, idxFile, operator):
    idxOpen = open('phase2output/{}'.format(idxFile), 'r')
    valueArray = []
    for lineIndex, line in enumerate(idxOpen):
        if line[0] != " " or line.find("/") == -1:
            continue
        else:
            if operator == "<" and line[1:-1] < key:
                value = next(idxOpen)[1:-1]
                valueArray.append(value)
            elif operator == ":" and line[1:-1] == key:
                value = next(idxOpen)[1:-1]
                valueArray.append(value)
            elif operator == ">" and line[1:-1] > key:
                value = next(idxOpen)[1:-1]
                valueArray.append(value)
            elif operator == ">=" and line[1:-1] >= key:
                value = next(idxOpen)[1:-1]
                valueArray.append(value)
            elif operator == "<=" and line[1:-1] <= key:
                value = next(idxOpen)[1:-1]
                valueArray.append(value)
    return valueArray

def processWord(word):
    operator = None
    lookFor = None
    lookIn = None
    if len(word) == 0:
        return 1
    while word[0] == " ":
        word = word[1:]
    colonIndex = word.find(":")
    lessThanEqualToIndex = word.find("<=")
    lessThanIndex = word.find("<")
    greaterThanIndex = word.find(">")
    greaterThanEqualToIndex = word.find(">=")
    if colonIndex != -1:
        operator = ":"
        lookFor = word[colonIndex+1:].lower()
        while lookFor[0] == " ":
            lookFor = lookFor[1:]
        if word.find("date") == 0:
            lookIn = "date"
        elif word.find("subj") == 0:
            lookIn = "subj"
        elif word.find("body") == 0:
            lookIn = "body"
        elif word.find("from") == 0:
            lookIn = "from"
        elif word.find("to") == 0:
            lookIn = "to"
        elif word.find("cc") == 0:
            lookIn = "cc"
        elif word.find("bcc") == 0:
            lookIn = "bcc"
        else:
            print("Invalid argument(s). Please try again.")
            return 1

    elif lessThanIndex != -1 and lessThanEqualToIndex == -1:
        operator = "<"
        lookFor = word[lessThanIndex+1:].lower()
        if word.find("date") == 0:
            lookIn = "date"
        else:
            print("Invalid argument(s). Please try again.")
            return 1
    elif greaterThanIndex != -1 and greaterThanEqualToIndex == -1:
        operator = ">"
        lookFor = word[greaterThanIndex+1:].lower()
        if word.find("date") == 0:
            lookIn = "date"
        else:
            print("Invalid argument(s). Please try again.")
            return 1

    elif lessThanEqualToIndex != -1:
        operator = "<="
        lookFor = word[lessThanIndex+2:].lower()
        if word.find("date") == 0:
            lookIn = "date"
        else:
            print("Invalid argument(s). Please try again.")
            return 1
    elif greaterThanEqualToIndex != -1:
        operator = ">="
        lookFor = word[greaterThanIndex+2:].lower()
        if word.find("date") == 0:
            lookIn = "date"
        else:
            print("Invalid argument(s). Please try again.")
            return 1

    #Search terms case
    if operator == None:
        lookFor = word
        if lookFor[-1] == "%":
            rowids = parseregexidx(lookFor, "te.idx")
        else:
            rowids = parseidx(lookFor, "te.idx")
        return rowids

    if lookIn == "subj" or lookIn == "body":
        if lookFor[-1] == "%":
            roughrowids = parseregexidx(lookFor, "te.idx")
            rowids = []
            for roughrowid in roughrowids:
                records = parseidx(roughrowid, "re.idx")
                for record in records:
                    if parseregexRecord(record, lookIn, lookFor) == True and (roughrowid not in rowids):
                        rowids.append(roughrowid)
        else:
            roughrowids = parseidx(lookFor, "te.idx")
            rowids = []
            for roughrowid in roughrowids:
                records = parseidx(roughrowid, "re.idx")
                for record in records:
                    if parseRecord(record, lookIn, lookFor) == True and (roughrowid not in rowids):
                        rowids.append(roughrowid)
        return rowids

    #Search emails case
    elif lookIn == "to" or lookIn == "from" or lookIn == "cc" or lookIn == "bcc":
        lookIn_lookFor = "{}-{}".format(lookIn, lookFor)
        rowids = parseidx(lookIn_lookFor, "em.idx")
        return rowids

    #Search dates case
    elif lookIn == "date":
        rowids = parsedateidx(lookFor, "da.idx", operator)
        return rowids

quitProgram = False
output = "brief"
while quitProgram != True:
    command = ""
    command = input("").lower()
    if command == "output=full":
        if output == "full":
            print("Output already in full mode!")
        elif output == "brief":
            output = "full"
            print("Output changed to full mode.")
    elif command == "output=brief":
        if output == "brief":
            print("Output already in brief mode!")
        elif output == "full":
            output = "brief"
            print("Output changed to brief mode.")
    
    spaceArray = [-1]
    [spaceArray.append(m.start()+1) for m in re.finditer('[a-z0-9] +[a-z0-9]', command)]
    rowidQueries = []
    for i in range(len(spaceArray)):
        
        startIndex = spaceArray[i]+1
        if i == len(spaceArray)-1:
            thisWord = processWord(command[startIndex:])
            if thisWord != 1:
                rowidQueries.append(thisWord)
        else:
            endIndex = spaceArray[i+1]
            thisWord = processWord(command[startIndex:endIndex])
            if thisWord != 1:
                rowidQueries.append(thisWord)

    rowidQueries.sort(key=len)
    finalRowidQuery = []
    for rowID in rowidQueries[0]:
        inAllArrays = True
        for rowIdQuery in rowidQueries:
            if rowID not in rowIdQuery:
                inAllArrays = False
                break
        if inAllArrays == True:
            finalRowidQuery.append(rowID)
        else:
            continue
    if output == "full":
        for finalRowID in finalRowidQuery:
            print(parseidx(finalRowID, "re.idx"))

    elif output == "brief":
        for finalRowID in finalRowidQuery:
            recordArr = parseidx(finalRowID, "re.idx")
            record = recordArr[0]
            startStr = record.find("<subj>") + 6
            endStr = record.find("</subj>")
            subject = record[startStr:endStr]
            print("{} {}".format(finalRowID, subject))