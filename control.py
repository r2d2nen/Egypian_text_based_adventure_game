#!/usr/bin/python

verificationString="gsisdhtncooaqrbstuobtusoyieigjp ten"
eggs= [' ', ' ', ' ', ' ', ' ']


for i0 in xrange(7):
    for i1 in xrange(5):
        eggs[i1] = eggs[i1] + verificationString[0]
        verificationString=verificationString[1:]
        

print eggs



