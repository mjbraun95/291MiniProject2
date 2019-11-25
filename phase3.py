from bsddb3 import db
import bsddb3
import re
import os

def parseRecord(record,lookIn,lookFor):
    startStr = "<{}>".format(lookIn)
    start = record.find(startStr)
    endStr = "</{}>".format(lookIn)
    end = record.find(endStr)
    print("record[start:end]: {}".format(record[start:end]))
    if record[start:end].lower().find(lookFor) != -1:
        print("Found <{}>{}!".format(lookIn,lookFor))
        return True
    else:
        return False

def parseidx(key, idxFile):
    idxOpen = open('phase2output/{}'.format(idxFile), 'r')
    valueArray = []
    for lineIndex, line in enumerate(idxOpen):
        # print("line[0]: {}".format(line[0]))
        if line[0] != " ":
            # print("meta stuff")
            continue
        else:
            if line[1:-1].lower() == key:
                print("match found in {} for {} on line {}!".format(idxFile, key,lineIndex))
                # print("next(idxOpen)[1:-1]: {}".format(next(idxOpen)[1:-1]))
                value = next(idxOpen)[1:-1]
                valueArray.append(value)
    return valueArray

def parsedateidx(key, idxFile, operator):
    idxOpen = open('phase2output/{}'.format(idxFile), 'r')
    valueArray = []
    for lineIndex, line in enumerate(idxOpen):
        # print("line[0]: {}".format(line[0]))
        if line[0] != " " or line.find("/") == -1:
            # print("meta stuff")
            continue
        else:
            if operator == "<" and line[1:-1] < key:
                print("match found in {} for {} {} {} on line {}!".format(idxFile, line[1:-1], operator, key,lineIndex))
                value = next(idxOpen)[1:-1]
                valueArray.append(value)
            elif operator == ":" and line[1:-1] == key:
                print("match found in {} for {} {} {} on line {}!".format(idxFile, line[1:-1], operator, key,lineIndex))
                value = next(idxOpen)[1:-1]
                valueArray.append(value)
            elif operator == ">" and line[1:-1] > key:
                print("match found in {} for {} {} {} on line {}!".format(idxFile, line[1:-1], operator, key,lineIndex))
                value = next(idxOpen)[1:-1]
                valueArray.append(value)

    return valueArray

def processWord(word):
    colonIndex = word.find(":")
    lessThanIndex = word.find("<")
    greaterThanIndex = word.find(">")

    if colonIndex != -1:
        operator = ":"
        lookFor = word[colonIndex+1:].lower()
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

    elif lessThanIndex != -1:
        operator = "<"
        lookFor = word[lessThanIndex+1:].lower()
        if word.find("date") == 0:
            lookIn = "date"
        else:
            print("Invalid argument(s). Please try again.")
            return 1
    elif greaterThanIndex != -1:
        operator = ">"
        lookFor = word[greaterThanIndex+1:].lower()
        if word.find("date") == 0:
            lookIn = "date"
        else:
            print("Invalid argument(s). Please try again.")
            return 1

    #Search terms case
    else:
        rowids = parseidx(word, "te.idx")
        print("rowids: {}".format(rowids))
        return rowids
    if lookIn == "subj" or lookIn == "body":
        roughrowids = parseidx(lookFor, "te.idx")
        rowids = []
        for roughrowid in roughrowids:
            records = parseidx(roughrowid, "re.idx")
            for record in records:
                if parseRecord(record, lookIn, lookFor) == True:
                    rowids.append(roughrowid)
        print("rowids: {}".format(rowids))
        return rowids

    #Search emails case
    elif lookIn == "to" or lookIn == "from" or lookIn == "cc" or lookIn == "bcc":
        lookIn_lookFor = "{}-{}".format(lookIn, lookFor)
        rowids = parseidx(lookIn_lookFor, "em.idx")
        print("rowids: {}".format(rowids))
        return rowids

    #Search dates case
    elif lookIn == "date":
        rowids = parsedateidx(lookFor, "da.idx", operator)
        print("rowids: {}".format(rowids))
        return rowids
    
quitProgram = False
output = "full"
while quitProgram != True:
    command = ""
    command = input("")
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
    [spaceArray.append(m.start()) for m in re.finditer(' ', command)]
    # print("spaceArray: {}".format(spaceArray))
    rowidQueries = []
    for i in range(len(spaceArray)):
        
        startIndex = spaceArray[i]+1
        if i == len(spaceArray)-1:
            print("----\nCHECKING WORD {}\n----".format(command[startIndex:]))
            thisWord = processWord(command[startIndex:])
            if thisWord != 1:
                rowidQueries.append(thisWord)
        else:
            endIndex = spaceArray[i+1]
            print("----\nCHECKING WORD {}\n----".format(command[startIndex:endIndex]))
            thisWord = processWord(command[startIndex:endIndex])
            if thisWord != 1:
                rowidQueries.append(thisWord)
    rowidQueries.sort(key=len)
    for index, rowIdQuery in enumerate(rowidQueries):
        print("rowidQueries[{}]: {}".format(index, rowIdQuery))
