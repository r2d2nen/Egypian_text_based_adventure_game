#!/usr/bin/python
import random, string

def createverification(inputList):
    verification = ""
    
    #at least 5 element in list
    for ix in xrange(5):
        if len(inputList)<=5:
            inputList.append("".join([random.choice(string.lowercase) for i in xrange(6)]))
    
    #at least 5 characters in each element
    for ix in xrange(5):
        while len(inputList[-(ix+1)])<=8:
            inputList[-(ix+1)] = inputList[-(ix+1)] + random.choice(string.lowercase)
    
    #Take the i letter from the last 5 easter eggs i = [0,4]
    for i0 in xrange(7):
        for i1 in xrange(5):
            verification = verification + inputList[-(i1+1)][i0]
    
    return verification

easterEggsFound= ['Hatt', 'Rope', 'MC Dog', '404', ' ', 'pyramid', 'lysande']
name = "R2"

#Append the score and verification string to the file verification file
with open('scorex.txt', 'a') as txt:
    txt.write('\n' + str(len(easterEggsFound)) + '  ' + name + '  ' + createverification(easterEggsFound))
