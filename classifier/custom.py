import re

def getPatternCount(inputString, pattern):
    r = re.findall(pattern, inputString)
    length = len(r)
    return length

def removeRegex(inputString, pattern):
    r = re.findall(pattern, inputString)
    for i in r:
        inputString = re.sub(i, '', inputString)
    return inputString