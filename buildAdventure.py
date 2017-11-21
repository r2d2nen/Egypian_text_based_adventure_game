#Text based adventure game

#Read this first
""" 
This is a text based adventure game written for the purpose to learn the basics in python. This is my first python program and therefore not so well organized. In this game one can wonder around to explore, kill monsters and find easter eggs. Some special commands can be found by typing "special commands" while plying."""

from sys import exit
import time
import re #To count numbers
import random 

# importin music to the game. Here is the music mode set
musicMode = "off"
if musicMode == "on":
    import vlc
    music1 = vlc.MediaPlayer("Jones.mp3") #Indiana Jones
    music2 = vlc.MediaPlayer("MovingCastle.mp3") #Background music
    music3 = vlc.MediaPlayer("Invincible.mp3") #Fighting music
    music4 = vlc.MediaPlayer("NyanCat.mp3") #Nyan cat
    music5 = vlc.MediaPlayer("Unicorn.mp3") #Robot unicorn_

#rooms contains: items, doors pointing in direction
rooms = [
         [["pyramid", "sand", "gate", "cactus" ], [0]],
         [["statue", "painting", "bug"],[0, 1, 3]],
         [["skeleton", "spider web", "slime"],[0, 3]],
         [["shovel", "potion", "hoe", "vine"],[0, 1, 3]],
         [["pergament scroll", "spices", "baskets"],[0, 2]],
         [["mummy", "toilet paper", "bleach bottle"],[1, 2]],
         [["ra", "anubis", "thot", "osiris" ],[1, 2, 3]],
         [["sarcophagus", "fountain"],[2, 3]],
         [["giant spider","treasure","mysterious door" ],[2]],
         [["sphinx", "big cat","grumpy cat","nyan cat"],[0, 1]]
        ]

#global variables
bag = ["torch", "rope", "cake"]
tooHeavy = [
    "vine","painting", "sarcophagus", "big cat", "ra", "anubis", "thot", "osiris", "statue", "bug", "fountain","big cat", "hidden door"]
notDropAble = []
hand = []
speakJoseph = 0
lastRoom = 0
currentRoom = 0
torchLit = False
lastInput = "  temp  "
plentyBugs = False
statueWhole = True
unavalibleMove = False
easterIsComing = False
easterEggsFound = []
ableToLeave = False
takenNose = False
sarcophagusOpen = False
timesTalkedWeirdMan = 0
toxicated = False
eggsFound = False
listAt = "room"

if musicMode == "on":
    currentMusic = music1
    
riddle = [
"""There are two sisters:
one gives birth to the other and she,
in turn, gives birth to the first.
Who are the two sisters?""",
"""Which creature has one voice and yet becomes
four-footed and two-footed and three-footed?
What am I?""",
"""I'm the ruler of shovels, 
I have a wife, 
I have a double, 
And I'm as thin as a knife.
What am I""",
"""Born in the flame 
Conceived in the earth
Some use me with shame 
And others with mirth
Once I've been tamed I hardly miss
And all men fear my deadly cold kiss 
They cloak themselves in shells and chains 
They try to fend off the inevitable pain 
I am gifted to both soldiers and kings 
My beauty can rival an angels wings 
But do not forget the homely hearth 
For it was probably my first place of birth
What am I?""",
"""I have wood but no bark,
leaves that don't fall
I am made up of branches, 
and I come in sizes of all. 
I am completely devoured many times, 
over and over by a worm of a kind. 
If you desire to know the answer of mine,
look for the secret that I've stored inside.
What am I?""",
"""I have holes but holds water.
What am I?""",
"""If you look you cannot see me.
And if you see me you cannot see anything else.
I can make anything you want happen,
but later everything goes back to normal.
What am I?""",
"""I never was,
am always to be.
No one ever saw me,
nor ever will.
And yet I am the confidence of all,
To live and breathe on this terrestrial ball.
What am I?""",
"""The one who makes it, sells it.
The one who buys it, never uses it.
The one that uses it never knows that he's using it.
What am I?""",
"""What does man love more than life
Fear more than death or mortal strife
What the poor have, the rich require,
and what contented men desire,
What the miser spends and the spendthrift saves
And all men carry to their graves?
What am I?""",
"""It walks on four legs in the morning,
two legs at noon,
and three legs in the evening.
What am I?""",
"""I have a head,
a tail,
is brown,
and have no legs.
What am I?""",
"""Tear one off and scratch my head,
what once was red is black instead.
What am I?""",
"""Round like an apple,
deep like a cup,
yet all the king's horses can not pull me up.
What am I?""",
"""If I were to ask the Queen and the chair
Both to tell me what they were,
And then should beg of you to bear
To the top of the house the Queen and her chair,
The Queen, her chair, and yourself, all three,
In the same sentence would answer me.
What is that sentence?""",
"""I love to climb up high in trees,
digging holes, and feeling the breeze.
I eat eggs, apples, carrots, meat,
even peanut butter, is a treat.
Around the world, my kin are found.
"Chirping" is our signature sound.
What am I?""",
"""If I were to bleed from a wound or two,
You'd note in amazement, my blood is blue.
I'm found as a fossil in ancient stone,
Yet living today, I'm almost a clone.
My eyes will adjust a great many fold,
To see by the moonlight, who I can hold.
If I could tell my mate, I would say it is true,
These wonderful eyes are only for you.
I'm one of the last to die from pollution,
A living exception to evolution.
What am I?""",
"""As black as ink yet isn't ink,
As white as milk yet isn't milk,
As soft as silk yet isn't silk,
And hops about like a filly-foal.
What am I?""",
"""Now in this rhyme, you will find all the elements of a riddle,
All the clues are buried here, somewhere in the middle.
My first is in fact the last naturally to be seen,
I am in part a catalyst for refining gasoline.
My second is in party balloons they float up off the ground,
Although Noble I give your voice a tiny squeaking sound.
Equally noble is my third, I'm said to be mostly inert,
I'm used in incandescent lights so the filament won't get hurt.
My fourth is known as devilish stuff, of volcanoes I do smell,
Although no-one's been back to report, I'm supposed to stink like hell!
Finally I am used to make airplanes you can trust,
I'm light, I'm strong, I shine like new, I never, ever rust.
Put us all together, and you get what comes before,
Practice makes us perfect, go over it once more.
What am I?""",
"""My name states I'm a singular male,
I can have a number, a head, but no tail.
I've also great strength and I can be tough,
But I'll smooth things out when they are rough.
Although I go back to an age now gone,
I'm around today for everyone.
What am I?""",
"""My third in my first is most awful at sea,
Yet many outlive it, so therefore may we.
My first in my third is the charm of the wood
And type of whatever is noble and good:
Do you ask for my second? - I've mentioned it twice,
Nay, in these very lines you will meet with it thrice.
What am I?""",
"What falls but never breaks and breaks but never falls?"]

# 0 north, 1 east, 2 south 3 vest
faceDirection = 0

#Is it possible to go backwards
def ableBehind():
    global lastRoom
    if lastRoom == 0:
        return False
    else:
        return True

#Enables difrent colors on the terminal text.
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    #To use code like this, you can do something like
    #print bcolors.WARNING + "Warning: No active frommets remain. Continue?" + bcolors.ENDC

def compass(turn):
    global faceDirection
    if turn == "right":
        faceDirection = (faceDirection+1)%4
    elif trun == "left":
        faceDirection = (faceDirection-1)%4
    elif turn == "back":
        faceDirection = (faceDirection+2)%4
    else:
        print "ERROR turning"

# Checks if there is a monster in the current room.
def monsterInRoom():
    if "mummy" in rooms[currentRoom][0] or "giant spider" in rooms[currentRoom][0]:
        return True
    else:
        return False

#Informs the player if they found a new easter egg.
def newEgg(playerText):
    global easterEggsFound
    if playerText in easterEggsFound:
        return
    else:
        easterEggsFound.append(playerText)
        if easterIsComing == True:
            print "\nNice you found a new easter egg. Found %r" %(playerText)

#The player have finished the game.
def end():
    print("\n\nYay! You finished the game. But did you find all easter eggs?")
    print "Next time try the command \"special commands\" to learn new commands"
    print "You found %d easter egges in total." % (len(easterEggsFound))
    print "If you want to save your score sign with at least 2 letters.\n\n"
    
    name = raw_input("Name >>> ")
    if len(name) > 1:
        #Append the score to the score file
        with open('score.txt', 'a') as txt:
            txt.write('\n' + str(len(easterEggsFound)) + '  ' + name)
            
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
    
            #Take the i letter from the last 5 easter eggs i = [0,7]
            for i0 in xrange(7):
                for i1 in xrange(5):
                    verification = verification + inputList[-(i1+1)][i0]
            
            return verification

        #Append the score and verification string to the file verification file
        with open('scorex.txt', 'a') as txt:
            txt.write('\n' + str(len(easterEggsFound)) + '  ' + name + '  ' + createverification(easterEggsFound))
        
    print "\n \n"
    print(" ----------------------------------------\n")
    print("|     Thank you for playing my game      |")
    print("|   If you have feedback write it here   |")
    print("|      I might add it to the game        |")
    print("\n ----------------------------------------")
    print " \n \n"
    feedback()
    exit(0)
    
# transfers the player to next room. Input: current room, facing direction and direction the person is heading.
def changeRoom(room, facing, want):
    #the rows are in which way your facing [N,E,S,W,], then the matrix in side the rows are in which direction you want to go [F, R, L] (not backwards that we have a variable for). And the vector inside that is what room you enter depending on in which room you where before.#OBS! subtract one to current room in playerText print "input:", facing, want, room 
    matrix = [[[4,8,6,7,5,6,7,8,5] , [2,2,1,4,6,7,7,8,3] ,  [3,1,9,4,5,5,6,8,9]],
    
              [[2,2,1,4,6,7,7,8,3] , [1,2,3,1,9,3,4,2,9] , [4,8,6,7,5,6,7,8,5]],
     
              [[1,2,3,1,9,3,4,2,9] , [3,1,9,4,5,5,6,8,9] , [2,2,1,4,6,7,7,8,3]],
     
              [[3,1,9,4,5,5,6,8,9] , [4,8,6,7,5,6,7,8,5] , [1,2,3,1,9,3,4,2,9]]]
     
    return matrix[facing][want][room - 1]

# transform cardinal direction to normal direction
def doorFacing(personFacing):
    temp = []
    for item in rooms[currentRoom][1]:
        if item == personFacing:
            temp.append("Forward")
        elif item == (personFacing-1):
            temp.append("Left")
        elif item == (personFacing-2):
            temp.append("Behind")
        elif item == (personFacing-3):
            temp.append("Right")
        elif item == (personFacing+1):
            temp.append("Right")
        elif item == (personFacing+2):
            temp.append("Behind")
        elif item == (personFacing+3):
            temp.append("Left")
        else:
            print "Error in doordirection"
    print 'You see doors to the: ' '%s' '.'% ', '.join(map(str, temp))
    if currentRoom == 1 and ableToLeave == True:
        print "The gate is opened and you can now leave the pyramid."
        
def feedback():
    global currentRoom
    global lastInput
    feedback = raw_input(bcolors.OKGREEN +"Feedback >>> " +  bcolors.ENDC)
    if len(feedback) < 3:
        return
    feedback = feedback.lower()
    #Append the feedback to the file
    with open('feedback.txt', 'a') as txt:
        txt.write('\n\n' + feedback + ",         CURRENTROOM: " + str(currentRoom) + ",     Last input: " + lastInput)
    print "\n \n"
    print(" ----------------------------------------\n")
    print("|                                        |")
    print("|     Thank you for your feedback        |")
    print("|                                        |")
    print("\n ----------------------------------------")
    print " \n \n"
    
    unavalibleMove = True
    return

#When the player lose the game
def die():
    print "\n \n"
    print(" ----------------------------------------\n")
    print("|     Thank you for playing my game      |")
    print("|   If you have feedback write it here   |")
    print("|      I might add it to the game        |")
    print("\n ----------------------------------------")
    print " \n \n"
    feedback()
    exit(0)

#Music controler
def music(playerText):
    if musicMode == "on":
        global music1
        global music2
        global music3
        global music4
        global music5
        global unavalibleMove
        
        
        if "repeat" in playerText or "replay" in playerText:
            music("stop")
            currentMusic.play()
        elif "play" in playerText or "start" in playerText:
            music("stop")
            music2.play()
            currentMusic = music2
            return True
        elif "stop" in playerText or "paus" in playerText:
            music1.stop()
            music2.stop()
            music3.stop()
            music4.stop()
            music5.stop()
            return True
        else:
            return False
    return False

#Enables cheats to make the game testing faster
def cheat(playerText):
    bag.append(playerText)

def highScore():
    print " "
    txt = "score.txt"
    #txt = open(txt)

    with open(txt) as f_in:
        lines = (line.rstrip() for line in f_in) 
        lines = list(line for line in lines if line) # Non-blank lines in a list

    content = lines

    def sort(content):
        values = []
        for x in range(0, len(content)):
            values.append(int(content[x].split()[0]))
        if len(values)<= 1:
            return content
        elif len(values)>=2:
            midd = (float(sum(values)/len(values)))
            high = []
            low = []
            mean = []
            for i in range(0, len(content)):
                if values[i] > midd:
                    high.append(content[i])
                elif values[i] < midd:
                    low.append(content[i])
                else:
                    mean.append(content[i])
            return (sort(high)+mean+sort(low))
    
    sortedList =  sort(content)
    print "\n".join(sortedList)
    return True

#Lets the player generate code sugested to be added to the game
def generalAdd():
    firstO = True
    
    
    print "\n\nSoon you will be presented a promt\nwhere you can fill in want you want to have in your add.\n\"Verb\" and \"reply\" will allways be requiered, so please fill in them first.\n\n"
    
    
    verb = raw_input("Verb >>> ")
    if len(verb) < 1:
        return
    verb = verb.lower()
    
    text = raw_input("\n\nReply >>> ")
    
    print "\n\nNow for the specifics for your add.\nWhrite a character 2 times if you want two of those in your add.\nWrite zero or plenty of the following characters:"
    print "\n\"S\" to add a synonym to the object"
    print "\"O\" to add a object that must be present, and named"
    print "\"A\" to add a object to the game"
    print "\"R\" to remove a object from the game that is present"
    print "\"E\" to add a easter egg (use this responsibly)"
    print "\"X\" to add a explenation to the programer about this suggestion"
    
    #Player inserts what ze want to add
    want = raw_input("What do you want? >>> ")
    want = want.lower()
    
    
    #prepering syntax lines
    line1= "        elif \"" + verb + " \" in playerText"
    line2 = "            if" 
    line3 = "                print \"" + text + "\"\n"
    line4 = ""
    line5 = "            else:\n"
    line6 = "                print \"Hmm... I can't find it.\"\n"
    
    canChangeLater = True
    if "investigate" in verb or "inspect" in verb or "look at " in verb or "ins" == verb or "i" == verb:
        line1= "        elif investigate(playerText)"
        canChangeLater = False
    
    
    for x in want:
        if x == "o":
            print "\n"
            newObject = raw_input("Object >>> ")
            newObject = newObject.lower()
            line1 += " and \" " + newObject + "\" in playerText"
            if firstO == True:
                line2+="(\"" + newObject+ "\" in rooms[currentRoom][0] or \"" +newObject+"\" in bag)"
                firstO = False
            elif firstO == False:
                line2+=" and (\"" + newObject+ "\" in rooms[currentRoom][0] or \"" +newObject+"\" in bag)"
        elif x == "a":
            print "\n"
            newObject = raw_input("add Object >>> ")
            newObject = newObject.lower()
            line4+="                rooms[currentRoom][0].append(\"" +newObject+"\")\n"
        elif x == "r":
            print "\n"
            newObject = raw_input("remove Object >>> ")
            newObject = newObject.lower()
            line4+="                if \"" + newObject+ "\" in rooms[currentRoom][0]:\n                    rooms[currentRoom][0].remove(\"" + newObject + "\")\n                elif \"" + newObject+ "\" in bag:\n                    bag.remove(\"" + newObject + "\")\n"
        elif x == "e":
            print "\n"
            newObject = raw_input("Easer egg name >>> ")
            line4+="                newEgg(\"" +newObject+"\")\n"
        elif x == "x":
            print "\n"
            newObject = raw_input("Explaining >>> ")
            line4+="                #fix comment:" +newObject+"\n"
        elif x == "s":
            print "\n"
            newObject = raw_input("Synonym >>> ")
            line4+="                #fix Synonym: or \"" +newObject+"\" in playerText\n"
    
    
    line1+=":\n"
    line2+=":\n"
    
    #A special condition with no item interaction
    if "o" not in want:
        if canChangeLater:
            line1= "        elif \"" + verb + "\" == playerText:\n"
        line2 = ""
        line5 = ""
        line6 = ""
    
    write = line1 + line2 + line3 + line4 + line5 + line6
    
    print "\nDo you want to keep this? (\"Yes\", \"Y\" or just enter counts as a yes. \"No\" or \"N\" deletes this suggested add)\n"
    
    reply = raw_input("Save? >>> ")
    reply = reply.lower()
    if reply == "no" or reply == "n":
        return
    
    #Append the newObject to the file
    with open('readdyForAction.txt', 'a') as txt:
        txt.write('\n' + write)
    print "\n \n"
    print(" ----------------------------------------\n")
    print("|                                        |")
    print("|   Thank you for your new suggestion    |")
    print("|                                        |")
    print("\n ----------------------------------------")
    print " \n \n"
    
# This is options the player always has. 
def always(playerText):
    global torchLit
    global currentRoom
    global lastRoom
    global lastInput
    
    #All things you can pick up
    def pickUp(playerText):
        temp = playerText.split()
        if len(temp)>1:
            if temp[-1] in rooms[currentRoom][0]:
                if temp[-1] in tooHeavy:
                    print("%s is way too heavy."% temp[-1])
                elif temp[-1] == "door" or temp[-1] == "gate":
                    print "The %s is stuck to the pyramid"% temp[-1]
                    print "and you don't think you can lift the pyramid." + bcolors.OKBLUE + "do you?"
                    choice = raw_input("\n> " + bcolors.ENDC)
                    choice = choice.lower()
                    if "yes" in choice or "y" in choice:
                        print "Well this is not like a game where you can do such stuff ^^"
                    elif "no" in choice:
                        print "That's right. Now stop doing silly stuff"
                    else:
                        print "That's not a response i expected."
                else:
                    print("You picked up the %s"% temp[-1])
                    rooms[currentRoom][0].remove(temp[-1])
                    bag.append(temp[-1])
                    if temp[-1]== "pyramid":
                        newEgg("pyramid")
                    elif temp[-1]== "smell":
                        newEgg("smell")
            elif len(temp)>2:
                if (temp[-2] +" "+ temp[-1]) in tooHeavy:
                    print("%s is way too heavy."% (temp[-2] +" "+ temp[-1]))
                elif (temp[-2] +" "+ temp[-1]) in rooms[currentRoom][0]:
                    print("You picked up the %s"% (temp[-2] +" "+ temp[-1]))
                    rooms[currentRoom][0].remove((temp[-2] +" "+ temp[-1]))
                    bag.append((temp[-2] +" "+ temp[-1]))
                elif len(temp)>3:
                    if (temp[-3] +" "+ temp[-2] +" "+ temp[-1]) in tooHeavy:
                        print("%s is way too heavy."% (temp[-3] +" "+ temp[-2] +" "+ temp[-1]))
                    elif (temp[-3] +" "+ temp[-2] +" "+ temp[-1]) in rooms[currentRoom][0]:
                        print("You picked up the %s"% (temp[-3] +" "+ temp[-2] +" "+ temp[-1]))
                        rooms[currentRoom][0].remove((temp[-3] +" "+ temp[-2] +" "+ temp[-1]))
                        bag.append((temp[-3] +" "+ temp[-2] +" "+ temp[-1]))
                    elif len(temp)>4:
                        if (temp[-4] +" "+ temp[-3] +" "+ temp[-2] +" "+ temp[-1]) in tooHeavy:
                            print("%s is way too heavy."% (temp[-4] +" "+ temp[-3] +" "+ temp[-2] +" "+ temp[-1]))
                        elif (temp[-4] +" "+ temp[-3] +" "+ temp[-2] +" "+ temp[-1]) in rooms[currentRoom][0]:
                            print("You picked up the %s"% (temp[-4] +" "+ temp[-3] +" "+ temp[-2] +" "+ temp[-1]))
                            rooms[currentRoom][0].remove((temp[-4] +" "+ temp[-3] +" "+ temp[-2] +" "+ temp[-1]))
                            bag.append((temp[-4] +" "+ temp[-3] +" "+ temp[-2] +" "+ temp[-1]))
            else:
                print "NO! The", temp[-1], "could not be found"
            return True
    
    #All things you can drop
    def drop(playerText):
        global torchLit
        temp = playerText.split()
        if len(temp)>1:
            if temp[-1] == "slime" and "slime" in bag:
                print "You can't even pick it up from the bag"
            elif temp[-1] == "handflower" and "handflower" in bag:
                print "You can't drop the handflower.\nYou think that this is weird.\n(And the programmer thinks this is weird)"
            elif temp[-1] in bag:
                print"You dropped the", temp[-1]
                rooms[currentRoom][0].append(temp[-1])
                bag.remove(temp[-1])
            elif  temp[-1] in hand:
                print"You dropped the", temp[-1], "that you held"
                rooms[currentRoom][0].append(temp[-1])
                if temp[-1] == "torch":
                    torchLit = False
                hand.remove(temp[-1])
                newEgg("black out")
            elif len(temp)>2:   
                if (temp[-2] +" "+ temp[-1]) in bag:
                    print("You dropped the %s"% (temp[-2] +" "+ temp[-1]))
                    rooms[currentRoom][0].append((temp[-2] +" "+ temp[-1]))
                    bag.remove((temp[-2] +" "+ temp[-1]))
                elif len(temp)>3:
                    if (temp[-3] +" "+ temp[-2] +" "+ temp[-1]) in bag:
                        print("You dropped the %s"% (temp[-3] +" "+ temp[-2] +" "+ temp[-1]))
                        rooms[currentRoom][0].append((temp[-3] +" "+ temp[-2] +" "+ temp[-1]))
                        bag.remove((temp[-3] +" "+ temp[-2] +" "+ temp[-1]))
                    elif len(temp)>4:
                        if (temp[-4] +" "+ temp[-3] +" "+ temp[-2] +" "+ temp[-1]) in bag:
                            print("You dropped the %s"% (temp[-4] +" "+ temp[-3] +" "+ temp[-2] +" "+ temp[-1]))
                            rooms[currentRoom][0].append((temp[-4] +" "+ temp[-3] +" "+ temp[-2] +" "+ temp[-1]))
                            bag.remove((temp[-4] +" "+ temp[-3] +" "+ temp[-2] +" "+ temp[-1]))
            elif "bag" in playerText:
                print "No! You may not drop your bag."
            else:
                print "NO! The", temp[-1], " could not be found"
            return True
        elif "drop" == playerText:
                print "Just drop? You have to be more informative then that."
    
    def takeNose():
        global takenNose
        print "HaHa, got your nose!"
        if takenNose == False:
            bag.append("nose")
            takenNose = True
        newEgg("got nose")
      
    #Occurs often enough that it erns a method of its' own.
    def investigate(text):
        if "investigate" in text or "inspect" in text or "look at " in text or "ins" == text.split()[0] or "i" == text.split()[0]:
            return True
        else:
            return False
         
    #Nobody expects spanish inqusition!
    def spanishInqusition():
        newEgg("inqusition")
        print "\n\n\n\n"
        print "The door flies open and Cardinal Ximinez of Spain enters"
        print " "
        print "NOBODY EXPECTS THE SPANISH INQUSITION!"
        print "\n"
        print "Ximinez:", bcolors.OKBLUE,"Do you have a treasure on you?"
        ans =  raw_input("> " +  bcolors.ENDC)
        if "yes" in ans or "y" in ans:
            print "The spanish inqusition takes the treasure and leaves."
            bag.remove("treasure")
        else:
            print "Ximinez: Well that's awkward..."
            print "\nThe spanish inqusition leaves\n\n\n"
    
    #Kill command
    def kill(playerText):
        global unavalibleMove
        global ableToLeave
        #Can we kill the monster in the room
        if ("mummy" in playerText or "spider" in playerText or "monster" in playerText) and monsterInRoom():
            if "sword" in playerText:
                if "sword" in bag:
                    if "mummy" in playerText and "mummy" in rooms[currentRoom][0]:
                        print "Congrats! you killed the mummy,"
                        print "the curse is now lifted and you can return home from your expedition."
                        ableToLeave = True
                        rooms[currentRoom][0].remove("mummy")
                        print "The mummy vaporizes."
                        print "All that remains is a pile of sand."
                        rooms[currentRoom][0].append("sand")
                    elif "spider" in playerText and "giant spider" in rooms[currentRoom][0]:
                        print "Congrats! you killed the giant spider"
                        print "A gnome enters and removes the dead spider"
                        rooms[currentRoom][0].remove("giant spider")
                    elif "monster" in playerText and ("mummy" in rooms[currentRoom][0] or "giant spider" in rooms[currentRoom][0]):
                        if "mummy" in rooms[currentRoom][0]:
                            print "Congrats! you killed the mummy"
                            print "the curse is now lifted and you can return home from your expedition."
                            ableToLeave = True
                            rooms[currentRoom][0].remove("mummy")
                            print "The mummy vaporizes."
                            print "All that remains is a pile of sand."
                            rooms[currentRoom][0].append("sand")
                            
                        elif "giant spider" in rooms[currentRoom][0]:
                            print "Congrats! you killed the giant spider"
                            print "A gnome enters and removes the dead spider"
                            rooms[currentRoom][0].remove("giant spider")
                else:
                    print "You don't have a sword"
            elif "torch" in playerText:
                if "mummy" in playerText and "mummy" in rooms[currentRoom][0]:
                    print "Congrats! you killed the mummy"
                    print "the curse is now lifted and you can return home from your expedition."
                    ableToLeave = True
                    rooms[currentRoom][0].remove("mummy")
                elif "spider" in playerText and "giant spider" in rooms[currentRoom][0]:
                    print "Congrats! you killed the giant spider"
                    print "A gnome enters and removes the dead spider"
                    rooms[currentRoom][0].remove("giant spider")
                elif "monster" in playerText and ("mummy" in rooms[currentRoom][0] or "giant spider" in rooms[currentRoom][0]):
                        if "mummy" in rooms[currentRoom][0]:
                            print "Congrats! you killed the mummy"
                            print "the curse is now lifted and you can return home from your expedition."
                            ableToLeave = True
                            rooms[currentRoom][0].remove("mummy")
                            print "The mummy vaporizes."
                            print "All that remains is a pile of sand."
                            rooms[currentRoom][0].append("sand")
                        elif "giant spider" in rooms[currentRoom][0]:
                            print "Congrats! you killed the giant spider"
                            print "A gnome enters and removes the dead spider"
                            rooms[currentRoom][0].remove("giant spider")
                            
            elif "sword" in bag:
                if "mummy" in playerText and "mummy" in rooms[currentRoom][0]:
                    print "Congrats! you killed the mummy"
                    print "the curse is now lifted and you can return home from your expedition."
                    ableToLeave = True
                    rooms[currentRoom][0].remove("mummy")
                    print "The mummy vaporizes."
                    print "All that remains is a pile of sand."
                    rooms[currentRoom][0].append("sand")
                elif "spider" in playerText and "giant spider" in rooms[currentRoom][0]:
                    print "Congrats! you killed the giant spider"
                    print "A gnome enters and removes the dead spider"
                    rooms[currentRoom][0].remove("giant spider")
                elif "monster" in playerText and ("mummy" in rooms[currentRoom][0] or "giant spider" in rooms[currentRoom][0]):
                        if "mummy" in rooms[currentRoom][0]:
                            print "Congrats! you killed the mummy"
                            print "the curse is now lifted and you can return home from your expedition."
                            ableToLeave = True
                            rooms[currentRoom][0].remove("mummy")
                            print "The mummy vaporizes."
                            print "All that remains is a pile of sand."
                            rooms[currentRoom][0].append("sand")
                        elif "giant spider" in rooms[currentRoom][0]:
                            print "Congrats! you killed the giant spider"
                            print "A gnome enters and removes the dead spider"
                            rooms[currentRoom][0].remove("giant spider")
            else:
                print "You need a sword to kill this monster"
                unavalibleMove = True
        elif "bug" in playerText or "cat" in playerText:
            print "No! You dont want to kill this cute animal."
        elif "anubis" in playerText and ("anubis" in rooms[currentRoom][0] or "anubis" in bag):
            print "You can't kill the statue of Anubis."
            print "But the spirit of Anubis doesn't approve of your actions"
            if len(bag)>0:
                print "and threrefore takes a item from you."
                bag.remove(bag[-1])
            else:
                print "and threrefore takes a item from you."
                print "What, you have no items in your bag!"
                print "DIE YOUR FOOL!"
                die()
        else:
            print "That's not a monster, or you can't find your intended target"
        return True
    
    
    #For all special spageti code. Warning this is a mess. Generated by all players of this game.
    def special(playerText):
        global currentRoom
        global lastRoom
        global faceDirection
        global unavalibleMove
        global ableToLeave
        global torchLit
        global plentyBugs
        global statueWhole
        global sarcophagusOpen
        global timesTalkedWeirdMan
        global toxicated
        global listAt
        global speakJoseph
        
        
        if "help" == playerText or "info" == playerText:
            print " \n"
            print(" -----------------------------------------\n")
            print("|   Here are some avilable commands:     |")
            print("|                                        |")
            print("|    \"open bag\"                   (bag)  |")
            print("|    \"search room\"                  (s)  |")
            print("|    \"take\"                         (t)  |")
            print("|    \"drop\"                         (d)  |")
            print("|    \"inspect (object)\"             (i)  |")
            print("|    \"enter left door\"              (l)  |")
            print("|    \"enter right door\"             (r)  |")
            print("|    \"enter forward door\"           (f)  |")
            print("|    \"enter behind door\"            (b)  |")
            print("|                                        |")
            print("|    \"feedback\" to leave your feedback   |")
            print("|                                        |")
            print("\n -----------------------------------------")
        
        elif ("light" in playerText or "fire"  in playerText) and "torch" in playerText:
            if "torch" in bag:
                print("You light the torch and can now see in dark places. \n")
                bag.remove("torch")
                hand.append("torch")
                global torchLit
                torchLit = True
                print("You are in a room with %i doors"% len(rooms[currentRoom][1]))
                doorFacing(faceDirection)
                print 'You see: ' '%s' % ', '.join(map(str, rooms[currentRoom][0]))
            else:
                print("NOOO! it is gone from the bag.")
        elif "easter egg" == playerText:
            print "" + "\n".join(easterEggsFound)
        elif "count" in playerText and ("sand" in playerText or "grains" in playerText) and ("sand" in rooms[currentRoom][0] or "sand" in bag):
            i=0
            while 1==1:
                i +=1
                if i == 17:
                    print bcolors.OKBLUE + "\nDo i have to continue?"
                    choice = raw_input("> "+ bcolors.ENDC)
                    choice = choice.lower()
                    if  "yes" == choice or "y" == choice:
                        print "\nWell... Okey."
                    else:
                        print "\nGood, it seem to be plenty of grains."
                        break
                if i>255:
                    print "You lost count of how manny grains you have counted"
                    print "this is pointless."
                    break
                elif i == 1:
                    print "\nSo far you have counted",i, "grain"
                else:
                    print "\nSo far you have counted",i, "grains"
                time.sleep(1)
        
        elif "hamon " in playerText and " cactus" in playerText:
            if("cactus" in rooms[currentRoom][0] or "cactus" in bag):
                print "You send your overflowing YELLOW BURST HAMON OVERDRIVU into the cactus. It explodes magnificently. Into several pieces. The cactus needles fly all over the place. "
                rooms[currentRoom][0].append("cactus piece")
                rooms[currentRoom][0].append("another cactus piece")
                rooms[currentRoom][0].append("cactus needles")
                if "cactus" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("cactus")
                elif "cactus" in bag:
                    bag.remove("cactus")
            else:
                print "Hmm... I can't find it."
        
        elif "generalise " in playerText and " general relativity" in playerText:
            if("general relativity" in rooms[currentRoom][0] or "general relativity" in bag):
                print "You discover Grand Unified Theory. Sehr GUT. Einstein is dancing in his grave. I think that's a good thing? Anyway, you get a price for a distinct absence of bells."
                rooms[currentRoom][0].append("grand unified theory")
                rooms[currentRoom][0].append("no bell price")
                if "general relativity" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("general relativity")
                elif "general relativity" in bag:
                    bag.remove("general relativity")
                newEgg("Physics NEEEEEEEEEEeEEEEEEEEErD")
                #fix comment:I know this is rather difficult to find. But I'm planning to create more clues, so that more people will find these easter eggs :3
            else:
                print "Hmm... I can't find it."
                
        elif investigate(playerText) and " door" in playerText and currentRoom != 0:
            print "This door looks like all the other doors. I bether not get lost in here"
        
        elif investigate(playerText) and " potion" in playerText:
            if ("potion" in rooms[currentRoom][0] or "potion" in bag):
                print "There seems to be a thick floating black liquid inside this brown glass bottle. "
            else:
                print "Hmm... I can't find it."
        
        elif "walk forward" == playerText:
            print "you take a tiny step forward"
            
        elif "walk left" == playerText:
            print "you take a tiny step left"
        
        elif "walk right" == playerText:
            print "you take a tiny step right"
         
        
        elif "grow " in playerText and " baby dinosaur" in playerText:
            if("baby dinosaur" in rooms[currentRoom][0] or "baby dinosaur" in bag):
                print "In order for the baby dinosaur to grow you need to feed it with something."
                #fix Synonym: or "" in playerText
            else:
                print "Hmm... I can't find it."

        elif "feed " in playerText and " baby dinosaur" in playerText and " cake" in playerText:
            if("baby dinosaur" in rooms[currentRoom][0] or "baby dinosaur" in bag) and ("cake" in rooms[currentRoom][0] or "cake" in bag):
                print "The baby dinosaur grows upp to become Puff the magic dragon"
                if "baby dinosaur" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("baby dinosaur")
                elif "baby dinosaur" in bag:
                    bag.remove("baby dinosaur")
                rooms[currentRoom][0].append("magic dragon")
                if "cake" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("cake")
                elif "cake" in bag:
                    bag.remove("cake")
            else:
                print "Hmm... I can't find it."

        elif "talk " in playerText and " joseph" in playerText:
            if("joseph" in rooms[currentRoom][0] or "joseph" in bag):
                if speakJoseph == 0:
                    speakJoseph = 1
                    print "\"He-llo? Could you say that again? More slowly? In a language I understand? Depending on what you said, I might kick your ass! Oh, so that's what you said. Well then.\" He continues to pose. After a while he gets bored with being the designated poser and goes and fetches a replacement, who looks like quite a delinquent! "
                    rooms[currentRoom][0].append("jotaro")
                    #fix comment:There should be some kind of if-statement here. Want different dialogue second time
                elif speakJoseph == 1:
                    print "\"Hello again\", he says while contorting his body in ways you thought were impossible. \"Could you perhaps do me a favour? I am veery thirsty, and would like something to drink. Preferably coke, but if you can't find anything better I might settle with some suspicious potion lying about in this pyramid or something. Not that anything like that exists.\""
                   #fix comment:This should happen the second time you speak to joseph
                
            else:
                print "Hmm... I can't find it."
                
                
        

        elif "give " in playerText and " joseph" in playerText and " potion" in playerText:
            if("joseph" in rooms[currentRoom][0] or "joseph" in bag) and ("potion" in rooms[currentRoom][0] or "potion" in bag):
                print "You give Joseph the potion. He drinks the potion. Suddenly he is wearing a dress and carrying large bottles of tequila. You are unsure how this happened. As a reward for your efforts he gives you an ancient piece of arcane knowledge: \"If ever you want to discover a Grand Unified Theory, you can try generalising general relativity, which can be found by promoting a general.\" 'tis good and genuine ancient knowledge."
                if "potion" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("potion")
                elif "potion" in bag:
                    bag.remove("potion")
            else:
                print "Hmm... I can't find it."

        elif "poke " in playerText and " joseph" in playerText:
            if("joseph" in rooms[currentRoom][0] or "joseph" in bag):
                print "You try to poke Joseph in the stomach. \"Ha, I knew you were going to poke me! Now you'll question why that matters, since you're going to do that anyway\". You say what he said that you'd say. \"I have already replaced my stomach with a cactus!\" You poke the cactus stomache. Your finger stings."
            else:
                print "Hmm... I can't find it."

        elif investigate(playerText) and " handflower" in playerText:
            if("handflower" in rooms[currentRoom][0] or "handflower" in bag):
                print "A neat flower that grows from your hand. It's very pretty."
            else:
                print "Hmm... I can't find it."


        elif "eat " in playerText and " handflower" in playerText:
            if("handflower" in rooms[currentRoom][0] or "handflower" in bag):
                print "You eat the flower. It grows back. There is no escape. "
            else:
                print "Hmm... I can't find it."
                
        

        elif "pet " in playerText and " joseph" in playerText:
            if("joseph" in rooms[currentRoom][0] or "joseph" in bag):
                print "\"I anticipated that you were going to do that, and have already switched places with you!\" Suddenly, you are the one being pet. You purr softly. "
            else:
                print "Hmm... I can't find it."



        elif "adore " in playerText and " duck" in playerText:
            if("duck" in rooms[currentRoom][0] or "duck" in bag):
                print "Well, now you've spent some  precious time drolling over a rubber duck. Please come to your senses and move on. "
            else:
                print "Hmm... I can't find it."

        elif ("light match" == playerText or "light a match" in playerText):
                print "You have no matches, funny enough"

        elif "put " in playerText and " egg" in playerText and " birds nest" in playerText:
            if("egg" in rooms[currentRoom][0] or "egg" in bag) and ("birds nest" in rooms[currentRoom][0] or "birds nest" in bag):
                print "\"No, I want to do the Easter bunny happy\""
            else:
                print "Hmm... I can't find it."

        elif "eat " in playerText and " joseph" in playerText:
            if("joseph" in rooms[currentRoom][0] or "joseph" in bag):
                print "You try to eat Joseph, but he has already smeared himself with batmans shark repellent spray. And since you are part shark, you are unable to eat him. "
            else:
                print "Hmm... I can't find it."
        
        elif "escape " in playerText and " handflower" in playerText:
            if("handflower" in rooms[currentRoom][0] or "handflower" in bag):
                print "You try to escape. But there is no escape."
            else:
                print "Hmm... I can't find it."

        elif "eat " in playerText and " jonathan" in playerText:
            if("jonathan" in rooms[currentRoom][0] or "jonathan" in bag):
                print "His muscles crunch between your teeth. Ending the Joestar bloodline sure feels great! I am certain nothing bad will come of this, and that they won't at all be needed to save the world."
                if "jonathan" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("jonathan")
                elif "jonathan" in bag:
                    bag.remove("jonathan")
            else:
                print "Hmm... I can't find it."

        elif "kill " in playerText and " jonathan" in playerText:
            if("jonathan" in rooms[currentRoom][0] or "jonathan" in bag):
                print "You use your eyelasers, a power which you of course have had from the beginning, to pierce Jonathan's brain. Ending the Joestar bloodline sure feels great! I am certain nothing bad will come of this, and that they won't at all be needed to save the world."
                if "jonathan" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("jonathan")
                elif "jonathan" in bag:
                    bag.remove("jonathan")
            else:
                print "Hmm... I can't find it."

        elif "pose " in playerText and " jonathan" in playerText:
            if("jonathan" in rooms[currentRoom][0] or "jonathan" in bag):
                print "You pose together with Jonathan. You look very fabulous together. It's a bonding experience."
            else:
                print "Hmm... I can't find it."

        elif investigate(playerText) and " joseph" in playerText:
            if("joseph" in rooms[currentRoom][0] or "joseph" in bag):
                print "Why is he standing like that? And how is he contorting his body like that?! Is it even possible?! "
            else:
                print "Hmm... I can't find it."

        elif "feed " in playerText and " baby dinosaur" in playerText and " sword" in playerText:
            if("baby dinosaur" in rooms[currentRoom][0] or "baby dinosaur" in bag) and ("sword" in rooms[currentRoom][0] or "sword" in bag):
                print "The baby dinosaur grows upp to become t-rex"
                if "baby dinosaur" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("baby dinosaur")
                elif "baby dinosaur" in bag:
                    bag.remove("baby dinosaur")
                rooms[currentRoom][0].append("t-rex")
                if "sword" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("sword")
                elif "sword" in bag:
                    bag.remove("sword")
            else:
                print "Hmm... I can't find it."
         
        elif "walk backwards" == playerText:
            print "you take a tiny step backward"
        
        elif "anubis" in playerText and "skeleton" in playerText and ("anubis" in rooms[currentRoom][0] or "anubis" in bag) and ("skeleton" in rooms[currentRoom][0] or "skeleton" in bag):
            if "skeleton" in rooms[currentRoom][0]:
                rooms[currentRoom][0].remove("skeleton")
            else:
                bag.remove("skelton")
            print "Anubis likes your gift and gives you a mummy"
            bag.append("mummy")
            newEgg("mommy")
        elif "cheer" in playerText and "grumpy cat" in playerText:
            print "Grumpy cat doesn't approve."
        elif "easter is coming" == playerText:
            global easterIsComing
            easterIsComing = True
        elif ("exit" in playerText or "end" in playerText or "leave" in playerText or "home" in playerText) and ableToLeave == True:
            print "The end is near"
            time.sleep(1)
            end()
        elif ("patch" in playerText or "fix" in playerText or "debug" in playerText or "remove" in playerText or "mend" in playerText) and "bug" in playerText:
            if "bug" in bag or "bug" in rooms[currentRoom][0] and plentyBugs == False:
                print "Now there are 137 more bugs"
                newEgg("fix bug")
                plentyBugs = True
                for x in range(0, 135):
                    rooms[currentRoom][0].append("bug")
                return True
            elif "bug" in bag or "bug" in rooms[currentRoom][0] and plentyBugs == True:
                 if (rooms[currentRoom][0].count("bug")) > 1:
                     print "You removed a bug"
                     print (rooms[currentRoom][0].count("bug"))-1, " bugs to go"
                 rooms[currentRoom][0].remove("bug")
                 if plentyBugs == True and "bug" not in rooms[1][0] :
                     print "Thank you for removing all bugs. You get a...     "
                     time.sleep(3)
                     print "404 reward not found"
                     newEgg("404")
            else:
                print "There is no bugs to fix. This game is flawless"
        elif "find" in playerText and "fork" in playerText:
            print "The fork is an illusion"
            return True
        elif "enter behind door" == playerText or "behind"  == playerText or "b" == playerText:
            if ableBehind(): 
                temp = lastRoom
                lastRoom = currentRoom
                currentRoom = temp
                faceDirection = (faceDirection + 2)%4
                print "You entered a new room"
                listAt = "room"
                if currentRoom == 6:
                    if musicMode == "on":
                        music("stop")
                        music5.play()
                        currentMusic = music5
                if "treasure" in bag:
                    spanishInqusition()
                if torchLit == True:
                    print("You are in a room with %i doors"% len(rooms[currentRoom][1]))
                    doorFacing(faceDirection)
                
                    print 'You see: ' '%s' % ', '.join(map(str, rooms[currentRoom][0]))
                    
            else:
                print"There is no return now. Let's explore!"
        elif ("enter forward door" == playerText or "forward"  == playerText or "f" == playerText) and currentRoom > 0:
            if monsterInRoom():
                unavalibleMove = True
                print "The monster is blocking the door"
            elif currentRoom == changeRoom(currentRoom, faceDirection, 0):
                print "There is no door in front of you"
            else:
                lastRoom = currentRoom
                currentRoom = changeRoom(currentRoom, faceDirection, 0)
                if torchLit == True:
                    print "You entered a new room"
                    listAt = "room"
                    print("You are in a room with %i doors"% len(rooms[currentRoom][1]))
                    doorFacing(faceDirection)
                
                    print 'You see: ' '%s' % ', '.join(map(str, rooms[currentRoom][0]))
                    if currentRoom == 6:
                        if musicMode == "on":
                            music("stop")
                            music5.play()
                            currentMusic = music5
                else:
                    print "Since it dark you walked in to the wall."
                    print "You can't stand the pain and dies"
                    die()
                    
        
        elif investigate(playerText) and " generic invisible stuff" in playerText:
            if("generic invisible stuff" in rooms[currentRoom][0] or "generic invisible stuff" in bag):
                print "You can't see invisible stuff."
                rooms[currentRoom][0].append("invisible pickaxe")
                if "generic invisible stuff" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("generic invisible stuff")
                elif "generic invisible stuff" in bag:
                    bag.remove("generic invisible stuff")
            else:
                print "Hmm... I can't find it."

        elif "swing " in playerText and " sword" in playerText:
            if("sword" in rooms[currentRoom][0] or "sword" in bag):
                print "You swing your sword, sword. Even though it is not a diamond sword sword. You can not afford, 'ford, a diamond sword, sword."
                unavalibleMove = True
            else:
                print "Hmm... I can't find it."

        elif investigate(playerText) and " spider donut" in playerText:
            if("spider donut" in rooms[currentRoom][0] or "spider donut" in bag):
                print "A donut made with Spider Cider in the batter."
            else:
                print "Hmm... I can't find it."
                
        elif "cut " in playerText and " vine" in playerText:
            if("sword" in rooms[currentRoom][0] or "sword" in bag) and ("vine" in rooms[currentRoom][0] or "vine" in bag):
                print "That would take all day, And I'm no lumberjack."
            elif("sword" not in rooms[currentRoom][0] and "sword" not in bag) and ("vine" in rooms[currentRoom][0] or "vine" in bag):
                print "You have no sword to cut it down the vine with"
            else:
                print "Hmm... I can't find it."


        elif "lumberjack" in playerText:
            if("vine" in rooms[currentRoom][0] or "vine" in bag):
                print "You start to sing \"I'm a lumberjack and I'm OK\n I sleep all night and I work all day\"\nAnd then you hear an man's choir sing\n(He's a lumberjack and he's OK...\nExcept this is the wrong guy)"
            else:
                print "Hmm... I can't find it."
        
        elif ("enter left door" == playerText or "left"  == playerText or "l" == playerText) and currentRoom == 0:
            print "There is no door to the left"
        elif ("enter left door" == playerText or "left"  == playerText or "l" == playerText) and currentRoom > 0:
            if monsterInRoom():
                unavalibleMove = True
                print "The monster is blocking the door"
            elif currentRoom == changeRoom(currentRoom, faceDirection, 2):
                print "There is no door left of you"
            else:
                lastRoom = currentRoom
                currentRoom = changeRoom(currentRoom, faceDirection, 2)
                faceDirection = (faceDirection + 3)%4
                print "You entered a new room"
                listAt = "room"
                if torchLit == True:
                    print("You are in a room with %i doors"% len(rooms[currentRoom][1]))
                    doorFacing(faceDirection)
                
                    print 'You see: ' '%s' % ', '.join(map(str, rooms[currentRoom][0]))
                    if currentRoom == 6:
                        if musicMode == "on":
                            music("stop")
                            music5.play()
                            currentMusic = music5
                else:
                    print "Since it dark you walked in to the wall."
                    print "You can't stand the pain and dies"
                    die()
            return True
        elif ("enter right door" == playerText or "right"  == playerText or "r" == playerText) and currentRoom == 0:
            print "There is no door right of you"
        elif ("enter right door" == playerText or "right"  == playerText or "r" == playerText) and currentRoom > 0:
            if monsterInRoom():
                unavalibleMove = True
                print "The monster is blocking the door"
            elif currentRoom == changeRoom(currentRoom, faceDirection, 1):
                print "There is no door right of you"
            else:
                lastRoom = currentRoom
                currentRoom = changeRoom(currentRoom, faceDirection, 1)
                faceDirection = (faceDirection + 1)%4
                print "You entered a new room"
                listAt = "room"
                if torchLit == True:
                    print("You are in a room with %i doors"% len(rooms[currentRoom][1]))
                    doorFacing(faceDirection)
                
                    print 'You see: ' '%s' % ', '.join(map(str, rooms[currentRoom][0]))
                    if currentRoom == 6:
                        if musicMode == "on":
                            music("stop")
                            music5.play()
                            currentMusic = music5
                else:
                    print "Since it dark you walked in to the wall."
                    print "You can't stand the pain and dies"
                    die()
        
        

        elif "halp" == playerText:
                print "Stahp it Dolan!"

        elif "pet " in playerText and " kitty master" in playerText:
            if("kitty master" in rooms[currentRoom][0] or "kitty master" in bag):
                print "You consider petting the kitty master, and looks at this sublime being. The kitter master laughs in a friendly manner, sensing your thoughts. The kitty master pets you. You purr softly. The kitty master then proceeds to rub your belly. You are a good kitty and and do not attack him for this. Life is good. "
                newEgg("inner kitty")
            else:
                print "Hmm... I can't find it."
        
        elif "unprepare for the expedition" == playerText:
                print "No, this is exciting"
        
        elif "inspect" == playerText:
            print "inspect what? I don't know what you are thinking of. You have to tell me."
            
        elif "i'm thinking about" in playerText or "im thinking about" in playerText:
            print "I don't really care, now tell me what to do."
        
        elif "walk around pyramid" == playerText:
            print "You take a strol ending up where you started"
        
        elif "open" in playerText and "sarcophagus" in playerText:
            if ("sarcophagus" in rooms[currentRoom][0] or "sarcophagus" in bag):
                if sarcophagusOpen == False:
                    print "You take a look inside and finds a treasure and a duck."
                    rooms[currentRoom][0].append("treasure")
                    rooms[currentRoom][0].append("duck")
                    sarcophagusOpen = True
                elif sarcophagusOpen == True:
                    print "I't is still opened"
        
        elif "clear" == playerText:
            print"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
        
        elif "drink" in playerText and "vine" in playerText:
            if "vine" in rooms[currentRoom][0] or  "vine" in bag:
                print "You should learn how to spell \"wine\" :P"
            else:
                print "Hmm... I can't find it."
                
        elif "drink" in playerText and "wine" in playerText:
            if "vine" in rooms[currentRoom][0] or  "vine" in bag:
                print "There is no wine in this room, only a \"vine\""
                if "potion" in rooms[currentRoom][0] or  "potion" in bag:
                    print "But hey! I got a potion I can drink."
            else:
                print "Hmm... I can't find it."

        elif "drink" == playerText:
            print "Drink from what? Be more precise next time."
            
        elif "drink" in playerText and "fountain" in playerText:
            if "fountain" in rooms[currentRoom][0] or "fountain" in bag:
                print "Finally some water."
                if toxicated == True:
                    print "The holy fountain water removes the toxics in your body. You no more suffer the Blackconfusion"
                    toxicated = False
                
        elif "drink" in playerText and "bottle" in playerText:
            if "water bottle" in rooms[currentRoom][0] or "water bottle" in bag:
                print "Yuck! This water tastes bleach."
                bag.append("bleach bottle")
                if "water bottle" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("water bottle")
                elif "water bottle" in bag:
                    bag.remove("water bottle")
            else:
                print "Nothing to drink from."
        
        elif ("bleach bottle" in playerText or "bottle" in playerText) and ("fountain" in playerText or "water" in playerText) and ("fountain" in rooms[currentRoom][0] or "fountain" in bag) and ("bleach bottle" in rooms[currentRoom][0] or "bleach bottle" in bag):
            print "You now have a water bottle."
            bag.append("water bottle")
            bag.remove("bleach bottle")
            newEgg("water bottle")
        
        elif "walk" == playerText or "breath" == playerText or "die" == playerText or "jump" == playerText:
            print "Now you are being silly. ^^"
            print "I should not have to be ordered this."
        
        elif "climb" in playerText and "pyramid" in playerText and "pyramid" in rooms[currentRoom][0]:
            print "You climbed the pyramid and found a birds nest"
            rooms[currentRoom][0].append("birds nest")
        elif "special commands" == playerText:
            
            print "     easter egg         (reveals found easter eggs)"
            print "     easter is coming   (You will be informed when you find a easter egg)"
            print "     generalAdd  (gadd) (Add a general command to the game)"
            print "     CTRL + C           (This is cheating and not allowed)"
    
            if musicMode == "on":
                print """
                play music
                stop music
                replay music"""        
        
        elif "generaladd" == playerText or "gadd" == playerText:
            generalAdd()
            unavalibleMove = True
        
        #Here is some serious special code all genarated with the function generalAdd.py
        
        elif "cut " in playerText and " vine" in playerText and " sword" in playerText:
            if("vine" in rooms[currentRoom][0] or "vine" in bag) and ("sword" in rooms[currentRoom][0] or "sword" in bag):
                print "You cut down the vine and recieve fire wood =)"
                rooms[currentRoom][0].append("fire wood")
                if "vine" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("vine")
                elif "vine" in bag:
                    bag.remove("vine")
                #fix comment:mabye aparameter
            else:
                print "Hmm... I can't find it."

        elif "jump " in playerText and " rope" in playerText:
            if("rope" in rooms[currentRoom][0] or "rope" in bag):
                print "you jump with the rope"
            else:
                print "Hmm... I can't find it."
        

        elif "prepare for an expedition" == playerText:
                print "You rubb your belly and now feel well prepared."

        elif "hug " in playerText and " cactus" in playerText:
            if("cactus" in rooms[currentRoom][0] or "cactus" in bag):
                print "You embrace the cactus. The cactus does not return your affection. Ouch!"
                newEgg("desert hippie")
            else:
                print "Hmm... I can't find it."

        elif "hug" == playerText:
                print "You hug yourself. Perhaps you should find something else to hug?"

        
        elif "burn " in playerText and " cactus" in playerText:
            if("cactus" in rooms[currentRoom][0] or "cactus" in bag):
                print "You burn down the cactus and all that remins is some ash"
                if "cactus" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("cactus")
                elif "cactus" in bag:
                    bag.remove("cactus")
                rooms[currentRoom][0].append("ash")
            else:
                print "Hmm... I can't find it."
         
        elif investigate(playerText) and " cactus" in playerText:
            if("cactus" in rooms[currentRoom][0] or "cactus" in bag):
                print "This is a ordinary cactus, nothing special. \nNOTHING SPECIAL"
            else:
                print "Hmm... I can't find it."
        
        elif "feel around" == playerText:
                print "You feel somthing hard"
        
        elif investigate(playerText) and " ash" in playerText:
            if("ash" in rooms[currentRoom][0] or "ash" in bag):
                print "Black as ash, or what does one say?"
            else:
                print "Hmm... I can't find it."

        elif "war painting" in playerText:
            if("ash" in rooms[currentRoom][0] or "ash" in bag):
                print "Cool, you use the ash to make a awesome war painting in your face."
                if "ash" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("ash")
                elif "ash" in bag:
                    bag.remove("ash")
                newEgg("to war!")
            else:
                print "Hmm... I can't find it."
        
        elif "throw " in playerText and " cactus" in playerText:
            if("cactus" in rooms[currentRoom][0] or "cactus" in bag):
                print "The cactus' spikes get stuck to your hand. You put it back where you took it"
            else:
                print "Hmm... I can't find it."

        elif investigate(playerText) and " glass bottle" in playerText:
            if("glass bottle" in rooms[currentRoom][0] or "glass bottle" in bag):
                print "The glass bottle is plain brown, nothing fancy at all."
            else:
                print "Hmm... I can't find it."

        elif investigate(playerText) and " duck" in playerText:
            if("duck" in rooms[currentRoom][0] or "duck" in bag):
                print "A yellow rubber duck. How piculiar ^^\n And it has a small blue hat on its' head. How cute. "
            else:
                print "Hmm... I can't find it."

        elif "put " in playerText and " fountain" in playerText and " duck" in playerText:
            if("fountain" in rooms[currentRoom][0] or "fountain" in bag) and ("duck" in rooms[currentRoom][0] or "duck" in bag):
                print "You put the duck in the fountain. It floats nicly."
            else:
                print "Hmm... I can't find it."

        elif "hang yourselfe " in playerText:
            if("rope" in rooms[currentRoom][0] or "rope" in bag) and currentRoom != 0:
                print "You tie the rope to the seeling and around your neck.\n You jump from the top of your bag."
                if len(bag)>5:
                    print "Your atempt sucseeded."
                    die()
                else:
                    print "your bag is not full enough. You land softly on your feet. Diassapointed you untie yourself"
                    newEgg("suicide fail")
            else:
                print "Hmm... I can't find the right objects."

        elif ("present " in playerText or "give " in playerText) and " weird old man" in playerText and " sand castle" in playerText:
            if("weird old man" in rooms[currentRoom][0] or "weird old man" in bag) and ("sand castle" in rooms[currentRoom][0] or "sand castle" in bag):
                print "\"Understand this I do not. Take back castle you must\"\nThe weird old man does not accept your gift."
            else:
                print "Hmm... I can't find it."

        elif "antidote" == playerText:
                if toxicated:
                    print "Yes a antidote would be realy nice right now.\nLets search for one."
                else:
                    print bcolors.OKBLUE +"Antidote for what?"
                    choice = raw_input("\n> " + bcolors.ENDC)
                    choice = choice.lower()
                    print  "\""+choice+ "\" Na, that's nothing to wory about"
                    
        elif "puke" == playerText:
                if toxicated:
                    print "\"Puke... I don't know what that means.\""
                else:
                    print "I'm not going to puke. It's descusting"

        elif "remove spikes " in playerText:
            if("cactus" in rooms[currentRoom][0] or "cactus" in bag):
                print "Naa, I do not want to waste my time on that. I'm here to explore =)"
            else:
                print "Hmm... I can't find it."
        
        elif "hold " in playerText and "nose" in playerText:
            if("smell" in rooms[currentRoom][0] or "smell" in bag):
                print "You cant feel the smell anny more"
            else:
                print "Hmm... I can't find it."
        
        elif "spin" == playerText:
                print "You spin around plenty of times and feel a bit dizy. Hay that was fun"
                faceDirection = int(4*random.random())

        elif "smoke " in playerText and " cactus" in playerText:
            if("cactus" in rooms[currentRoom][0] or "cactus" in bag):
                print "You feel a sticky smell in your nose."
                if "cactus" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("cactus")
                elif "cactus" in bag:
                    bag.remove("cactus")
            else:
                print "Hmm... I can't find it."

        elif ("incubate " in playerText or "hatch" in playerText) and " egg" in playerText:
            if("egg" in rooms[currentRoom][0] or "egg" in bag):
                print "you gently put your warm  butt on the egg. It seem to be most pleased. You wait a while and the egg hatch into a baby dinosaur!"
                rooms[currentRoom][0].append("baby dinosaur")
                newEgg("dinosaur")
                if "egg" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("egg")
                elif "egg" in bag:
                    bag.remove("egg")
            else:
                print "Hmm... I can't find it."
                
        
        elif ("crack " in playerText or "destroy " in playerText or "open " in playerText )and " egg" in playerText:
            if("egg" in rooms[currentRoom][0] or "egg" in bag):
                print "The liquid inside is now smered over the ground. The shell seems useless so you throw them away."
                if "egg" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("egg")
                elif "egg" in bag:
                    bag.remove("egg")
            else:
                print "Hmm... I can't find it."

        elif investigate(playerText) and " baby dinosaur" in playerText:
            if("baby dinosaur" in rooms[currentRoom][0] or "baby dinosaur" in bag):
                print "The baby dinosaur is utterly adorable! It has really tiny feet! "
            else:
                print "Hmm... I can't find it."

        elif "go home" == playerText:
                print "It's a very long way home, and you don't want to walk all the way. So you stay for a little longer"

        elif "eat " in playerText and " cactus" in playerText:
            if("cactus" in rooms[currentRoom][0] or "cactus" in bag):
                print "you really don't feel like having all those spikes in your mouth."
            else:
                print "Hmm... I can't find it."

        elif "use " in playerText and " torch" in playerText:
            if("torch" in rooms[currentRoom][0] or "torch" in bag):
                print("You light the torch and can now see in dark places. \n")
                if "torch" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("torch")
                elif "torch" in bag:
                    bag.remove("torch")
                hand.append("torch")                
                torchLit = True
                print("You are in a room with %i doors"% len(rooms[currentRoom][1]))
                doorFacing(faceDirection)
                print 'You see: ' '%s' % ', '.join(map(str, rooms[currentRoom][0]))
            else:
                print "Hmm... I can't find it."

        elif "cover " in playerText and " sand" in playerText and " cactus" in playerText:
            if("sand" in rooms[currentRoom][0] or "sand" in bag) and ("cactus" in rooms[currentRoom][0] or "cactus" in bag):
                print "The cactus is now totaly covered in sand. But the cactus shakes of the sand again since it is properly trained in doing so"
            else:
                print "Hmm... I can't find it."
        
        elif "sand" in playerText and "cake" in playerText and "use " in playerText:
            if("sand" in rooms[currentRoom][0] or "sand" in bag) and ("cake" in rooms[currentRoom][0] or "cake" in bag):
                print "You ruined the cake, it is now a muddcake"
                if "cake" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("cake")
                elif "cake" in bag:
                    bag.remove("cake")
                bag.append("mudcake")
            else:
                print "Hmm... I can't find the tools."
        
        elif "sword" in playerText and "painting" in playerText and "use " in playerText:
            if ("sword" in rooms[currentRoom][0] or  "sword" in bag) and ("painting" in rooms[currentRoom][0] or  "painting" in bag):
                print "You ruin the Mona Lisa. Mona Lisa gets smeared all over the sword. Wait, is that a reference to something obscure? Maybe to another part of this game that you haven't found yet and now can't find in this playthrough?"
                if "painting" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("painting")
                elif "paining" in bag:
                    bag.remove("painting")
            else:
                print "Hmm... I can't find the tools."
        
        elif "cake" in playerText and "painting" in playerText and "use " in playerText:
            if ("cake" in rooms[currentRoom][0] or  "cake" in bag) and ("painting" in rooms[currentRoom][0] or  "painting" in bag):
                print "You smear the cake all over the Mona Lisa and ruin it. Even worse, you ruin the cake."
                rooms[currentRoom][0].append("ruined painting")
                if "cake" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("cake")
                elif "cake" in bag:
                    bag.remove("cake")
                if "painting" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("painting")
                elif "painting" in bag:
                    bag.remove("painting")
            else:
                print "Hmm... I can't find the tools."
        
        elif "use ring" == playerText or ("put on" in playerText and "ring" in playerText):
            if ("ring" in rooms[currentRoom][0] or  "ring" in bag):
                print "You have now put on the ring. You suddenly realise the ring is very precious to you! You are also slightly transparent and overwhelmed with a desire to rule them all!"
            else:
                print "Hmm... I can't find the tools."
        
        elif "torch" in playerText and ("giant spider" in playerText or "spider" in playerText):
            if "torch" in hand and ("giant spider" in rooms[currentRoom][0] or  "giant spider" in bag):
                print "Congrats! you killed the giant spider"
                print "A gnome enters and removes the dead spider. Then the gnome apparates away."
                rooms[currentRoom][0].remove("giant spider")
            else:
                print "Hmm... I haven't lit the torch."

        elif "torch" in playerText and "mummy" in playerText:
            if "torch" in hand and ("mummy" in rooms[currentRoom][0] or  "mummy" in bag):
                print "Congrats! you killed the mummy,"
                print "the curse is now lifted and you can return home from your expedition."
                ableToLeave = True
                rooms[currentRoom][0].remove("mummy")
                print "The mummy vaporizes."
                print "All that remains is a pile of sand."
                        
            else:
                print "Hmm... I can't find the tools."

        elif "sword" in playerText and "mummy" in playerText:
            if ("sword" in rooms[currentRoom][0] or  "sword" in bag) and ("mummy" in rooms[currentRoom][0] or  "mummy" in bag):
                print "Congrats! you killed the mummy,"
                print "the curse is now lifted and you can return home from your expedition."
                ableToLeave = True
                rooms[currentRoom][0].remove("mummy")
                print "The mummy vaporizes."
                print "All that remains is a pile of sand."
                rooms[currentRoom][0].append("sand")
            else:
                print "Hmm... I can't find the tools."
        
        elif "sword" in playerText and ("giant spider" in playerText or "spider" in playerText):
            if ("sword" in rooms[currentRoom][0] or  "sword" in bag) and ("giant spider" in rooms[currentRoom][0] or  "giant spider" in bag):
                print "Congrats! you killed the giant spider"
                print "A gnome enters and removes the dead spider"
                rooms[currentRoom][0].remove("giant spider")
            else:
                print "Hmm... I can't find the tools."
        
        elif "cake" in playerText and "kitty master" in playerText and "use " in playerText:
            if ("cake" in rooms[currentRoom][0] or  "cake" in bag) and ("kitty master" in rooms[currentRoom][0] or  "kitty master" in bag):
                print "You offer the cake as a gift to the kitty master. The kitty master eats the cake and enjoys it's taste. Then the kitty master conjures forth a new cake for you. This one is even tastier!"
            else:
                print "Hmm... I can't find the tools."
        
        elif "sword" in playerText and "statue" in playerText and "use " in playerText:
            if ("sword" in rooms[currentRoom][0] or  "sword" in bag) and ("statue" in rooms[currentRoom][0] or  "statue" in bag):
                print "You try to cut the statue with the sword. The statue grabs the sword with it's hands and takes it back."
                if "sword" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("sword")
                elif "sword" in bag:
                    bag.remove("sword")
                statueWhole = True
            else:
                print "Hmm... I can't find the tools."

        elif "smell" in playerText and "cake" in playerText and "use " in playerText:
            if ("smell" in rooms[currentRoom][0] or  "smell" in bag) and ("cake" in rooms[currentRoom][0] or  "cake" in bag):
                print "You create an interesting combination of smell and taste. Horrific, but interesting. You really regret this action. That cake would have been delicious."
                if "smell" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("smell")
                elif "smell" in bag:
                    bag.remove("smell")
            else:
                print "Hmm... I can't find the tools."

        elif "rope" in playerText and "kitty master" in playerText and "use " in playerText:
            if ("rope" in rooms[currentRoom][0] or  "rope" in bag) and ("kitty master" in rooms[currentRoom][0] or  "kitty master" in bag):
                print "You make a collar and leash out of the rope, put the collar around your neck, and offer yourself as a pet to the kitty master. The rest of your life is filled with happiness from being a pet to the kitty master. However, the kitty master lets you continue to explore if you wish."
            else:
                print "Hmm... I can't find the tools."

        elif "sword" in playerText and "super general" in playerText and "use " in playerText:
            if ("sword" in rooms[currentRoom][0] or  "sword" in bag) and ("super general" in rooms[currentRoom][0] or  "super general" in bag):
                print "You stab the super generals heart!"
                if "super general" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("super general")
                elif "super general" in bag:
                    bag.remove("super general")
                rooms[currentRoom][0].append("dead super general")
            else:
                print "Hmm... I can't find the tools."

        elif "sword" in playerText and "supreme general" in playerText and "use " in playerText:
            if ("sword" in rooms[currentRoom][0] or  "sword" in bag) and ("supreme general" in rooms[currentRoom][0] or  "supreme general" in bag):
                print "You cut off the supreme generals mustache. This is a vital organ for the supreme commander, so the supreme commander dies. "
                if "super general" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("super general")
                elif "super general" in bag:
                    bag.remove("super general")
                rooms[currentRoom][0].append("dead super general")
            else:
                print "Hmm... I can't find the tools."

        elif "sword" in playerText and "shogun" in playerText and "use " in playerText:
            if ("sword" in rooms[currentRoom][0] or  "sword" in bag) and ("shogun" in rooms[currentRoom][0] or  "shogun" in bag):
                print "You have an extended duel with the shogun. In the end you emerge victorious; the shogun has been slain. "
                if "shogun" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("shogun")
                elif "shogun" in bag:
                    bag.remove("shogun")
                rooms[currentRoom][0].append("dead shogun")
            else:
                print "Hmm... I can't find the tools."
                
        elif "sword" in playerText and "general" in playerText and "use " in playerText:
            if ("sword" in rooms[currentRoom][0] or  "sword" in bag) and ("general" in rooms[currentRoom][0] or  "general" in bag):
                print "You cut off the generals head!"
                if "general" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("general")
                elif "general" in bag:
                    bag.remove("general")
                rooms[currentRoom][0].append("dead general")
            else:
                print "Hmm... I can't find the tools."
        
        elif "sword" in playerText and "kitty master" in playerText and "use " in playerText:
            if ("sword" in rooms[currentRoom][0] or  "sword" in bag) and ("kitty master" in rooms[currentRoom][0] or  "kitty master" in bag):
                print "You show your sword to the kitty master. The kitty master says that it is a nice sword, and pats you on the head. You purr softly."
            else:
                print "Hmm... I can't find the tools."

        elif "general" in playerText and "sand castle" in playerText and ("use " in playerText or "put" in playerText):
            if ("general" in rooms[currentRoom][0] or  "general" in bag) and ("sand castle" in rooms[currentRoom][0] or  "sand castle" in bag):
                print "You put the general in the sand castle. The general takes charge of it, hires a small garrison,  and fortifies its defenses. The sand castle has now become a fortified sand castle."
                if "sand castle" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("sand castle")
                elif "sand castle" in bag:
                    bag.remove("sand castle")
                if "general" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("general")
                elif "general" in bag:
                    bag.remove("general")
                rooms[currentRoom][0].append("fortified sand castle")
            else:
                print "Hmm... I can't find the tools."

        elif "super commander" in playerText and "sand castle" in playerText and ("use " in playerText or "put" in playerText):
            if ("super commander" in rooms[currentRoom][0] or  "super commander" in bag) and ("sand castle" in rooms[currentRoom][0] or  "sand castle" in bag):
                print "The super commander takes command of the sand castle and hires a garrison to man it. The sand castle is fortified into a super sand castle."
                if "sand castle" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("sand castle")
                elif "sand castle" in bag:
                    bag.remove("sand castle")
                if "super commander" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("super commander")
                elif "super commander" in bag:
                    bag.remove("super commander")
                rooms[currentRoom][0].append("super sand castle")
            else:
                print "Hmm... I can't find the tools."

        elif "weird old man" in playerText and "nyan cat" in playerText and "use " in playerText:
            if ("weird old man" in rooms[currentRoom][0] or  "weird old man" in bag) and ("nyan cat" in rooms[currentRoom][0] or  "nyan cat" in bag):
                if timesTalkedWeirdMan == 2:
                    print "You introduce the weird old man to nyan cat (Nyan cat says \"NYAN\"). The weird old man looks really excited. \"So the source of the blessing, this is. Extraordinary, this is!\" He jumps around in circles happily. "
                    timesTalkedWeirdMan = 3
                else:
                    print "The weird old man shies away from you, he doesn't trust you enought. \"What are you trying to do? Asked for this, I have not!\""
            else:
                print "Hmm... I can't find the tools."
        
        elif "pet " in playerText and " jonathan" in playerText:
            if("jonathan" in rooms[currentRoom][0] or "jonathan" in bag):
                print "Jonathan curls into a small buff ball. You pet his muscles. They purr softly, while glowing slightly. A flower starts to grow from your hand. "
                bag.append("handflower")
                #fix comment:The handflower should be in bag, and difficult to get rid off
            else:
                print "Hmm... I can't find it."
        
        elif " basket" in playerText and " hat" in playerText and "use " in playerText:
            if ("baskets" in rooms[currentRoom][0] or  "baskets" in bag):
                print "You put a basket on your head and use it as a epic hat."
                newEgg("nice hat")
            else:
                print "Hmm... I can't find the tools."

        elif "scroll" in playerText and "thot" in playerText and "use " in playerText:
            if ("scroll" in rooms[currentRoom][0] or  "scroll" in bag) and ("thot" in rooms[currentRoom][0] or  "thot" in bag):
                print "The spirit of Thot thanks you for the gift."
                if "scroll" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("scroll")
                elif "scroll" in bag:
                    bag.remove("scroll")
            else:
                print "Hmm... I can't find the tools."
        
        elif "rope" in playerText and "ra" in playerText and ("rope" in rooms[currentRoom][0] or "rope" in bag) and ("ra" in rooms[currentRoom][0] or "ra" in bag) and "use " in playerText:
            if "ra" in tooHeavy:
                print "You toppled the statue and can now pick it up"
                tooHeavy.remove("ra")
                newEgg("statue god")
            elif "ra" not in tooHeavy:
                print "You have already toppled the statue."
        
        elif "rope" in playerText and "anubis" in playerText and ("rope" in rooms[currentRoom][0] or "rope" in bag) and ("anubis" in rooms[currentRoom][0] or "anubis" in bag) and "use " in playerText:
            if "anubis" in tooHeavy:
                print "You toppled the statue and can now pick it up"
                tooHeavy.remove("anubis")
                newEgg("statue god")
            elif "anubis" not in tooHeavy:
                print "You have already toppled the statue."
        
        elif "rope" in playerText and "thot" in playerText and ("rope" in rooms[currentRoom][0] or "rope" in bag) and ("thot" in rooms[currentRoom][0] or "thot" in bag) and "use " in playerText:
            if "thot" in tooHeavy:
                print "You toppled the statue and can now pick it up"
                tooHeavy.remove("thot")
                newEgg("statue god")
            elif "thot" not in tooHeavy:
                print "You have already toppled the statue."
        
        elif "rope" in playerText and "osiris" in playerText and ("rope" in rooms[currentRoom][0] or "rope" in bag) and ("osiris" in rooms[currentRoom][0] or "osiris" in bag) and "use " in playerText:
            if "osiris" in tooHeavy:
                print "You toppled the statue and can now pick it up"
                tooHeavy.remove("osiris")
                newEgg("statue god")
            elif "osiris" not in tooHeavy:
                print "You have already toppled the statue."
        
        elif "skeleton pun" in playerText and "grumpy cat" in playerText and "use " in playerText:
            if ("skeleton pun" in rooms[currentRoom][0] or  "skeleton pun" in bag) and ("grumpy cat" in rooms[currentRoom][0] or  "grumpy cat" in bag):
                print "The cat does not seem to appreciate the higher arts (i.e. puns). It grumpily answers \"You're not a skeleton, that doesn't even make any Sans.\""
            else:
                print "Hmm... I can't find the tools."
        

        elif "skeleton pun" in playerText and "grumpy cat" in playerText and "use " in playerText:
            if ("skeleton pun" in rooms[currentRoom][0] or  "skeleton pun" in bag) and ("grumpy cat" in rooms[currentRoom][0] or  "grumpy cat" in bag):
                print "The cat does not seem to appreciate the higher arts (i.e. puns). It grumpily answers \"You're not a skeleton, that doesn't even make any Sans.\""
            else:
                print "Hmm... I can't find the tools."

        elif "toilet paper" in playerText and "fountain" in playerText and "use " in playerText:
            if ("toilet paper" in rooms[currentRoom][0] or  "toilet paper" in bag) and ("fountain" in rooms[currentRoom][0] or  "fountain" in bag):
                print "There isn't enough toilet paper to soak up all the water."
            else:
                print "Hmm... I can't find the tools."

        elif "sand" in playerText and "toilet paper" in playerText and "use " in playerText:
            if ("sand" in rooms[currentRoom][0] or  "sand" in bag) and ("toilet paper" in rooms[currentRoom][0] or  "toilet paper" in bag):
                print "Congratulations! You have created sandpaper. I do not recommend using it as toilet paper."
                bag.append("sand paper")
                if "toilet paper" in bag:
                    bag.remove("toilet paper")
                else:
                    rooms[currentRoom][0].remove("toilet paper")
            else:
                print "Hmm... I can't find the tools."
        
        elif "hidden door" in playerText and "enter" in playerText:
            if "hidden door" in bag or "hidden door" in rooms[currentRoom][0]:
                print "You can't enter the hidden door since it is hidden ^^"
            else:
                print "I can't find it."
                
        elif "hidden door" in playerText and "open" in playerText:
            if "hidden door" in bag or "hidden door" in rooms[currentRoom][0]:
                print "You can't open the hidden door since it is hidden ^^"
            else:
                print "I can't find it."
        
        elif "sarcophagus" in playerText and ("sarcophagus" in rooms[currentRoom][0] or "sarcophagus" in bag) and "enter" in playerText:
            if sarcophagusOpen == False:
                print "You need to open it first"
                rooms[currentRoom][0].append("treasure")
            elif sarcophagusOpen == True:
                print "You enter the sarcophagus and close the lid."
                print "You take a nap."
                print "Five years have passed and you wake up and crawl out again."
        elif " bag" in playerText and "enter" in playerText:
            print "You are to big to fit in the bag. :P"
        elif " gate" in playerText and ableToLeave and "enter" in playerText:
            print "The end is near"
            time.sleep(1)
            end()
        
        elif " cake" in playerText and investigate(playerText):
            if "cake" in bag or "cake" in rooms[currentRoom][0]:
                print "The cake looks like a smiley,"
                print "with red sprinkles and candy on it."
            else:
                print "NOO! The cake is gone.",bcolors.OKBLUE , "You ate it did you!?!"
                choice = raw_input("\n> " + bcolors.ENDC)
                choice = choice.lower()
                if "yes" in choice or "yepp" in choice:
                    print "Good, then you should manage this expedition."
                elif "no" in choice:
                    print "Don't you lie to me!"
                else:
                    print "That's not a response i expected."
        elif " socks" in playerText and investigate(playerText):
            if "socks" in rooms[currentRoom][0] or  "socks" in bag:
                print "This is a very dirty sock, with some extra ordinary big holes."
            else:
                print "Hmm... I can't find it."
        
        elif " smell" in playerText and investigate(playerText):
            if "smell" in rooms[currentRoom][0] or  "smell" in bag:
                print "It's an intense pulsating brown smell."
            else:
                print "Hmm... I can't find it."

        elif " ghost" in playerText and investigate(playerText):
            if "ghost" in rooms[currentRoom][0] or  "ghost" in bag:
                print "Somewhat transparent. Also ghostly"
            else:
                print "Hmm... I can't find it."

        elif " super general" in playerText and investigate(playerText):
            if "super general" in rooms[currentRoom][0] or  "super general" in bag:
                print "Wow that mustache is HUGE!"
            else:
                print "Hmm... I can't find it."

        elif " supreme general" in playerText and investigate(playerText):
            if "supreme general" in rooms[currentRoom][0] or  "supreme general" in bag:
                print "You could probably knit several jumpers from the supreme generals mustache!"
            else:
                print "Hmm... I can't find it."

        elif " shogun" in playerText and investigate(playerText):
            if "shogun" in rooms[currentRoom][0] or  "shogun" in bag:
                print "The shogun looks very stern and somber. You can't help but feel respect for this person. Can there really be any rank higher than this?"
            else:
                print "Hmm... I can't find it."

        elif " kitty master" in playerText and investigate(playerText):
            if "kitty master" in rooms[currentRoom][0] or  "kitty master" in bag:
                print "This being is beyond all awesomeness. Because kittens are super kawaii! :3"
            else:
                print "Hmm... I can't find it."

        elif " hostile fortified sand castle" in playerText and investigate(playerText):
            if "hostile fortified sand castle" in rooms[currentRoom][0] or  "hostile fortified sand castle" in bag:
                print "The fortified sand castle is now at war with you. The garrison inside, and their general, hates you with an intense passion. "
            else:
                print "Hmm... I can't find it."

        elif " fortified sand castle" in playerText and investigate(playerText):
            if "fortified sand castle" in rooms[currentRoom][0] or  "fortified sand castle" in bag:
                print "This sand castle has had it's defenses fortified. It is manned by a small garrison, and is commanded by a general. "
            else:
                print "Hmm... I can't find it."
            
        elif " hostile super sand castle" in playerText and investigate(playerText):
            if "hostile super sand castle" in rooms[currentRoom][0] or  "hostile super sand castle" in bag:
                print "The inhabitants of this castle hates you with a burning passion. You see members of the garrison inside brandishing swords, bows, and arrows. "
            else:
                print "Hmm... I can't find it."

        elif " super sand castle" in playerText and investigate(playerText):
            if "super sand castle" in rooms[currentRoom][0] or  "super sand castle" in bag:
                print "This sand castle has received significant fortifications and is manned by a competent garrison. It is commanded by a super general. "
            else:
                print "Hmm... I can't find it."

        elif " mysterious door" in playerText and investigate(playerText):
            if "mysterious door" in rooms[currentRoom][0] or  "mysterious door" in bag:
                print "The door is filled with strange carvings in a weird language you do not recognize. You wonder what possibly be behind this door. "
            else:
                print "Hmm... I can't find it."

        elif " strange door" in playerText and investigate(playerText):
            if "strange door" in rooms[currentRoom][0] or  "strange door" in bag:
                print "The door is still really strange. But it no longer feels right to use a word like \"mysterious\" while describing it. Not since that weird old man came out through it. "
            else:
                print "Hmm... I can't find it."

        elif " weird old man" in playerText and investigate(playerText):
            if "weird old man" in rooms[currentRoom][0] or  "weird old man" in bag:
                print "This old man looks CRAZY. His eyes keep darting all over the place, and he fidgets with a high frequency. He is dressed all in rags, and smells really bad. You think that you hear him mutter something under his breath. You miss most of it, but there is one small part you kind of hear. You're not sure, but it sounded a bit like \"Cthulhu fhtagn\""
            else:
                print "Hmm... I can't find it."

        elif " smelly sock" in playerText and investigate(playerText):
            if "smelly sock" in rooms[currentRoom][0] or  "smelly sock" in bag:
                print "The horrendous smell from this old sock can be felt from across the room. It's colour is disturbing and alarming. "
            else:
                print "Hmm... I can't find it."

        elif " ceiling" in playerText and investigate(playerText):
                print "The ceiling is just that, a ceiling.\nNothing worth inspecting."
        
        elif " feet" in playerText and investigate(playerText):
                print "They smell funny!"
           
        
        elif ("use " in playerText or "put " in playerText) and " duck" in playerText and " treasure" in playerText:
            if("duck" in rooms[currentRoom][0] or "duck" in bag) and ("treasure" in rooms[currentRoom][0] or "treasure" in bag):
                print "You put the duck in the pile of treasure. Suddenly, a miracle occurs. The duck comes alive, sprouting a top hat and a tremendous greed. "
                rooms[currentRoom][0].append("scrooge mcduck")
                if "duck" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("duck")
                elif "duck" in bag:
                    bag.remove("duck")
            else:
                print "Hmm... I can't find it."
                
                
        
        elif "use " in playerText  and " potion" in playerText and " smell" in playerText:
            if("potion" in rooms[currentRoom][0] or "potion" in bag) and ("smell" in rooms[currentRoom][0] or "smell" in bag):
                print "You put the smell in the potion. Congratulations, you have created an even more worrying liquid!"
                rooms[currentRoom][0].append("smelly potion")
                if "potion" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("potion")
                elif "potion" in bag:
                    bag.remove("potion")
            else:
                print "Hmm... I can't find it."
                
        

        elif "talk " in playerText and " jonathan" in playerText:
            if("jonathan" in rooms[currentRoom][0] or "jonathan" in bag):
                print "\"Hello, my name is Jonathan. I am currently on an epic quest to defeat my archnemesis and save the world and so on. Perhaps... you could help me. I am in need of a powerful weapon to defeat the most fearsome of foes. I need... a smelly sock. I believe such can be found in this pyramid. There is a person behind a certain mysterious door who probably smells a lot. Perhaps if you help him out a bit he will reward you with a sock.\" "
            else:
                print "Hmm... I can't find it."

        elif investigate(playerText) and " jonathan" in playerText:
            if("jonathan" in rooms[currentRoom][0] or "jonathan" in bag):
                print "A big and friendly giant dressed in a collared shirt, breeches, and a pair of long socks with dress shoes. A nobleman by the looks of it. For some reason he is posing a bit. "
            else:
                print "Hmm... I can't find it."
           
        elif "knock " in playerText and " bizarre door" in playerText:
            if("bizarre door" in rooms[currentRoom][0] or "bizarre door" in bag):
                print "You knock on the bizarre door. It swings open and an enormous and muscular person enters the room."
                rooms[currentRoom][0].append("jonathan")
            else:
                print "Hmm... I can't find it."     
        
                
        elif "tickle" in playerText and " programmer" in playerText:
            print "The programmer giggles like child, and shouts \"BJOOOOORN, why did you add this to the game?!\""
        
        elif "i" == playerText:
                print "The empty set is the unique set having no elements; its size or cardinality is zero."
                newEgg(" ")
                
        elif " egg" in playerText and investigate(playerText):
            if "egg" in bag or "egg" in rooms[currentRoom][0]:
                print "It is a big white egg with large green spots on it. The egg feels warm."
                newEgg("egg")
            else:
                print "Sorry but I can't inspect what's not here"
        
        elif " birds nest" in playerText and investigate(playerText):
            if "birds nest" in bag or "birds nest" in rooms[currentRoom][0]:
                if not eggsFound:
                    print "It's full of feathers and contains plenty of eggs."
                    print "You distribute the eggs in the surroundings"
                    rooms[currentRoom][0].append("egg")
                    rooms[currentRoom][0].append("egg")
                    rooms[currentRoom][0].append("egg")
                    eggsFound = True
                else:
                    print "It's full of feathers and contains no eggs."
            else:
                print "Sorry but I can't inspect what's not here"
        elif " rope" in playerText and investigate(playerText):
            if "rope" in bag or "rope" in rooms[currentRoom][0]:
                print "It's light brown and approximately 10 meters long."
            else:
                print "You trow up. Ooh! My rope. I got it ... back?!?."
                print (bcolors.OKBLUE + "Do you really want a description. Really...")
                newEgg("nice rope")
                bag.append("rope")
                choice = raw_input("\n> " + bcolors.ENDC)
                choice = choice.lower()
                if "yes" in choice or "y" in choice:
                    print "Well its not light brown anny more ^^"
                elif "no" in choice:
                    print "Thought so ^^"
                else:
                    print "That's not a response i expected."
        
        elif " bag" in playerText and investigate(playerText):
                print "Whoo! its actually very large."
                print "Wonder how manny things i can fit in it."
                print "Looks like maybe 536,870,912"
                print "...No wonder it feels heavy"
                newEgg("nice bag")
        
        elif " torch" in playerText and investigate(playerText):
            if "torch" in bag or "torch" in rooms[currentRoom][0] or "torch" in hand:
                print "The torch is made of an oak stick and some towels"
                print "Hopefully it lasts the whole expedition"
            else:
                print "Whuut! This should not be possible"
                newEgg("broke physics")
        
        elif " pyramid" in playerText and investigate(playerText):
            if "pyramid" in bag or  "pyramid" in rooms[currentRoom][0]:
                print "It looks like a stairway to heaven"
                print "The pyramid's design, with the majority of the weight closer to the ground,"
                print "and with the pyramidion on top means that less material higher"
                print "up on the pyramid will be pushing down from above."
                print "This distribution of weight allowed early"
                print "civilizations to create stable monumental structures."
            else:
                print "The inside is very cool. Look at all these hieroglyphs"
        
        elif (" sand" in playerText  and "paper" not in playerText) and investigate(playerText):
            if "sand" in bag or "sand" in rooms[currentRoom][0]:
                print "Sand sand sand, it's everywhere"
                print "Crazy that infinity is even more than all these grains"
            else:
                print "Finally no sand. Sorry but i can't inspect what's not here"
        
        elif " gate" in playerText and investigate(playerText):
            if "gate" in bag or "gate" in rooms[currentRoom][0]:
                print "The gate was beautiful once upon a time."
                print "What is left of the fancy designs and iron bars is covered in rust"
                print "and polished away by sand."
            else:
                print "Sorry but I can't inspect what's not here"
        
        elif " statue" in playerText and investigate(playerText):
           if "statue" in bag or "statue" in rooms[currentRoom][0]:
                print "This must be the guardian of the Pharaoh."
                if "sword" not in bag:
                    print "Its sword looks to be made of real iron."
                else:
                    print "It's missing its sword"
                if  "sword" not in bag and "sword" not in rooms[currentRoom][0]:
                    rooms[currentRoom][0].append("sword")
           else:
                print "Hmm... I can't find it."
        
        elif " sword" in playerText and investigate(playerText):
            if "sword" in bag or "sword" in rooms[currentRoom][0]:
                print "ooh! This sword have rubies on the handle,"
                print "and it's still sharp."
            else:
                print "Hmm... I can't find it."
            
        elif " painting" in playerText and investigate(playerText):
           if "painting" in bag or "painting" in rooms[currentRoom][0]:
                print "Dafuq... Mona Lisa!? But...  You shouldn't be here!"
                print "Mona Lisa walks away. A Hidden door was behind Mona Lisa"
                newEgg("mona lisa")
                rooms[currentRoom][0].remove("painting")
                rooms[currentRoom][0].append("hidden door")
           else:
                print "Hmm... I can't find it."
        
        elif " bug" in playerText and investigate(playerText):
            if ("bug" in bag or "bug" in rooms[currentRoom][0]) and plentyBugs == False:
                print "oooooooh! It's an Animalia Arthropoda Hexapoda Insecta Geotrupidae"
                print "I thought those were extinct"
            elif ("bug" in bag or "bug" in rooms[currentRoom][0]) and plentyBugs == True:
                print "Ooh! This looks like a hard fixed bug."
                print "Wonder what part of the code that is broken."
            else:
                print "Hmm... I can't find it."
        
        elif " hidden door" in playerText and investigate(playerText):
           if "hidden door" in bag or "hidden door" in rooms[currentRoom][0]:
                print "This is a nice piece of hidden door, therefore you can't find it."
                print "But you know exactly where you can't find it ^^"
           else:
                print "Hmm... I can't find it."
        
        elif " skeleton" in playerText and investigate(playerText):
            if "skeleton" in bag or "skeleton" in rooms[currentRoom][0]:
                print "This it not a human skeleton. but still."
                print "The skeleton must be from a mammal"
            else:
                print "Hmm... I can't find it."
        
        elif " spider web" in playerText and investigate(playerText):
            if "spider web" in bag or "spider web" in rooms[currentRoom][0]:
                print "This is so much web it could be the world wide web."
                print "But seriously. This is creepy."
            else:
                print "Hmm... I can't find it."
        
        elif " slime" in playerText and investigate(playerText):
            if "slime" in bag or "slime" in rooms[currentRoom][0]:
                print "This green slime looks like rancid fat."
                print "I got a feeling this doesn't bode well."
            else:
                print "Hmm... I can't find it."
        
        elif " treasure" in playerText and investigate(playerText):
            if "treasure" in bag or "treasure" in rooms[currentRoom][0]:
                print "Gold, gold. Plenty of gold."
                print "Lets search the other rooms too."
            else:
                print "Hmm... I can't find it."
        
        elif " sarcophagus" in playerText and investigate(playerText):
            if "sarcophagus" in bag or "sarcophagus" in rooms[currentRoom][0]:
                print "A sarcophagus acts like an outer shell to protect the mummy."
            else:
                print "Hmm... I can't find it."
        
        elif " shovel" in playerText and investigate(playerText):
            if "shovel" in bag or "shovel" in rooms[currentRoom][0]:
                print "This shovel was used thousands of years ago to farm."
            else:
                print "Hmm... I can't find it."
        
        elif " hoe" in playerText and investigate(playerText):
            if "hoe" in bag or "hoe" in rooms[currentRoom][0]:
                print "This hoe was used thousands of years ago to farm."
            else:
                print "Hmm... I can't find it."
        
        elif " vine" in playerText and investigate(playerText):
            if "vine" in bag or "vine" in rooms[currentRoom][0]:
                print "This vine covers the whole room."
                print "But how can it grow without sunlight?"
                print "Stupid game, no logic at all. "
            else:
                print "Hmm... I can't find it."
        
        elif (" scroll" in playerText or "pergament" in playerText) and investigate(playerText):
            if "pergament scroll" in bag or "pergament scroll" in rooms[currentRoom][0]:
                print "This scroll contains a list of some sort. Nothing you care to read right now."
            else:
                print "Hmm... I can't find it."
        
        elif " spices" in playerText and investigate(playerText):
            if "spices" in bag or "spices" in rooms[currentRoom][0]:
                print "Coriander, cinnamon, pepper and saffron."
            else:
                print "Hmm... I can't find it."
        
        elif " baskets" in playerText and investigate(playerText):
            if "baskets" in bag or "baskets" in rooms[currentRoom][0]:
                print "These eight baskets are looking fine."
            else:
                print "Hmm... I can't find it."
        
        elif " mummy" in playerText and investigate(playerText):
            if "mummy" in bag or "mummy" in rooms[currentRoom][0]:
                print "This mummy sure looks new. The toilet paper is still bleach white."
                newEgg("inspect dangerous")
        
        elif " toilet paper" in playerText and investigate(playerText):
            if "toilet paper" in bag or "toilet paper" in rooms[currentRoom][0]:
                print "Lambi, softer for the skin and with cute lambs on it."
            else:
                print "Hmm... I can't find it."
        
        elif " bleach bottle" in playerText and investigate(playerText):
            if "bleach bottle" in bag or "bleach bottle" in rooms[currentRoom][0]:
                print "This bottle is empty."
            else:
                print "Hmm... I can't find it."
        
        elif " ra" in playerText and investigate(playerText):
            if "ra" in bag or "ra" in rooms[currentRoom][0]:
                print "This is a statue of Ra, god of the sun.\nRa was king of the gods until Osiris took over his throne.\nHe is also known as Amun-Ra and Akmun-Rah."
            else:
                print "Hmm... I can't find it."
        
        elif " anubis" in playerText and investigate(playerText):
            if "anubis" in bag or "anubis" in rooms[currentRoom][0]:
                print "This is a statue of Anubis, god of dead, embalming, funerals, and mourning ceremonies.\nSon of Osiris and Memphis, Helps Osiris."
            else:
                print "Hmm... I can't find it."
        
        elif " thot" in playerText and investigate(playerText):
            if "thot" in bag or "thot" in rooms[currentRoom][0]:
                print "This is a statue of Thot, scribe god and god of wisdom."
            else:
                print "Hmm... I can't find it."
        
        elif " osiris" in playerText and investigate(playerText):
            if "osiris" in bag or "osiris" in rooms[currentRoom][0]:
                print "This is a statue of Osiris, god of the underworld and the afterlife.\nHusband and brother of Isis, Brother and mortal enemy to Seth,\n Father to Horus and Anubis."
            else:
                print "Hmm... I can't find it."
        
        elif " fountain" in playerText and investigate(playerText):
            if "fountain" in bag or "fountain" in rooms[currentRoom][0]:
                print "A stone fountain. It might be the fountain of youth"
            else:
                print "Hmm... I can't find it."
        
        elif " giant spider" in playerText and investigate(playerText):
            if "giant spider" in bag or "giant spider" in rooms[currentRoom][0]:
                print "A spider the size of carthorses, eight-eyed,"
                print "eight-legged, black, hairy, giantic."
                newEgg("inspect dangerous")
            else:
                print "Hmm... I can't find it."
        
        elif " big cat" in playerText and investigate(playerText):
            if "big cat" in bag or "big cat" in rooms[currentRoom][0]:
                print "     /\__/\ "
                print "    /`    '\ "
                print "  === 0  0 === "
                print "    \  --  / "
                print "   /        \ "
                print "  /          \ "
                print " |            | "
                print "  \  ||  ||  / "
                print "   \_oo__oo_/#######o"
            else:
                print "Hmm... I can't find it."
        
        elif " sphinx" in playerText and investigate(playerText):
            if "sphinx" in bag or "sphinx" in rooms[currentRoom][0]:
                print "This statue is a masterpiece. I get a bit jealous"
            else:
                print "Hmm... I can't find it."
        
        elif " grumpy cat" in playerText and investigate(playerText):
            if "grumpy cat" in bag or "grumpy cat" in rooms[currentRoom][0]:
                print "I enjoy life. I think I'll enjoy death even more."
            else:
                print "Hmm... I can't find it."
        
        elif " nyan cat" in playerText and investigate(playerText):
            if "nyan cat" in bag or "nyan cat" in rooms[currentRoom][0]:
                print "Gray cat with a pink toast, but why the smell.\n Aha! It's farting rainbows."
                if musicMode == "on":
                    music("stop")
                    music4.play()
                    currentMusic = music4
            else:
                print "Hmm... I can't find it."
        
        elif " nose" in playerText and investigate(playerText):
            if "nose" in bag or "nose" in rooms[currentRoom][0]:
                print "This nose is made of sandstone, and is really big."
            else:
                print "Hmm... I can't find it."
        
        elif " me" in playerText and investigate(playerText):
                print "I'm looking good ^^"
                print "Woaw, I'm wearing the same cloths as me."
        
        elif " general" in playerText and investigate(playerText):
            if "general" in rooms[currentRoom][0] or  "general" in bag:
                print "This general looks very serious and awe-inspiring. I mean, just look at the size of that mustache."
            else:
                print "Hmm... I can't find it."
        
        elif "eat " in playerText and " cake" in playerText:
            if "cake" in bag or rooms[currentRoom][0]:
                print "You eat the cake."
                if "cake" in bag:
                    bag.remove("cake")
                elif "cake" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("cake")
            else:
                print "NO! The cake is a lie."
        
        elif "general" in playerText and "eat " in playerText:
            if "general" in rooms[currentRoom][0] or  "general" in bag:
                print "Omnomnom. Very tasty general. You feel nourished. Too bad that you now have lots of mustache hair stuck in your teeth. "
                if "general" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("general")
                elif "general" in bag:
                    bag.remove("general")
            else:
                print "Hmm... I can't find it."

        elif "ghost" in playerText and "eat " in playerText and ("ghost" in rooms[currentRoom][0] or  "ghost" in bag):
            if "ghost" in rooms[currentRoom][0] or  "ghost" in bag:
                print "Your teeth pierce the exterior of the ghost. They meet no resistence. Because ghosts have no physical form. The ghost looks a bit scared of you."
            else:
                print "Hmm... I can't find it."

        elif "super general" in playerText and "eat " in playerText and ("super general" in rooms[currentRoom][0] or  "super general" in bag):
            if "super general" in rooms[currentRoom][0] or  "super general" in bag:
                print "This is super tasty!"
                if "super general" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("super general")
                elif "super general" in rooms[currentRoom][0]:
                    bag.remove("super general")
            else:
                print "Hmm... I can't find it."

        elif "supreme general" in playerText and "eat " in playerText:
            if "supreme general" in rooms[currentRoom][0] or  "supreme general" in bag:
                print "The nourishment you receive is truly supreme!"
                if "supreme general" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("supreme general")
                elif "supreme general" in bag:
                    bag.remove("supreme general")
            else:
                print "Hmm... I can't find it."

        elif "sand castle" in playerText and "eat " in playerText:
            if "sand castle" in rooms[currentRoom][0] or  "sand castle" in bag:
                print "Why did you do this? Sand isn't tasty. Your tounge is now really dry. This was not a pleasant experience :/"
                if "sand castle" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("sand castle")
                elif "sand castle" in bag:
                    bag.remove("sand castle")
            else:
                print "Hmm... I can't find it."

        elif "shogun" in playerText and "eat " in playerText:
            if "shogun" in rooms[currentRoom][0] or  "shogun" in bag:
                print "You try to eat the shogun. The shogun is not pleased, and with one mighty strike with a katana your head is shopped off. Decapitation happens to be lethal, so this is not good for you. "
            else:
                print "Hmm... I can't find it."

        elif "kitty master" in playerText and "eat " in playerText:
            if "kitty master" in rooms[currentRoom][0] or  "kitty master" in bag:
                print "You consider eating the kitty master. But then you remember that kittens are awesome and cute, and you change your mind. "
            else:
                print "Hmm... I can't find it."

        elif "mysterious door" in playerText and "eat " in playerText:
            if "mysterious door" in rooms[currentRoom][0] or  "mysterious door" in bag:
                print "You try to bite into the door. The door is really hard. Now your teeth hurt. "
            else:
                print "Hmm... I can't find it."

        elif "smelly sock" in playerText and "eat " in playerText:
            if "smelly sock" in rooms[currentRoom][0] or  "smelly sock" in bag:
                print "You force yourself into eating the smelly sock. The entire process is quite uncomfortable and painful. Your body does not appreciate this type of sustenance. You feel ill."
                if "smelly sock" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("smelly sock")
                elif "smelly sock" in rooms[currentRoom][0]:
                    bag.remove("smelly sock")
            else:
                print "Hmm... I can't find it."
                
        elif "omelet" in playerText and "eat " in playerText and ("omelet" in rooms[currentRoom][0] or  "omelet" in bag):
            if "omelet" in rooms[currentRoom][0] or  "omelet" in bag:
                print "You eat the omelet. You dislike the taste."
                if "omelet" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("omelet")
                elif "omelet" in bag:
                    bag.remove("omelet")
            else:
                print "Hmm... I can't find it."
        
        elif " coriander" in playerText and "eat " in playerText:
            if "coriander" in rooms[currentRoom][0] or  "coriander" in bag:
                print "You dig in on the Coriander... Beautiful butterflies hatch in your gut. You are now happy!"
            else:
                print "Hmm... I can't find it."

        elif " ra" in playerText and "eat " in playerText:
            if "ra" in rooms[currentRoom][0] or  "ra" in bag:
                print "You can't fit the whole statue in your mouth."
            else:
                print "Hmm... I can't find it."

        elif " food" in playerText and "eat " in playerText:
            if "food" in rooms[currentRoom][0] or  "food" in bag:
                print "Just what I needed."
                if "food" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("food")
                elif "food" in bag:
                    bag.remove("food")
            else:
                print "Hmm... I can't find it."

        elif " me" in playerText and "eat " in playerText or "self" in playerText and "eat " in playerText:
                print "Eating your self would change nothing to the better."

        elif " monster" in playerText and "eat " in playerText:
            if "monster" in rooms[currentRoom][0] or  "monster" in bag:
                print "It's more likely that you will be eaten."
            else:
                print "Hmm... I can't find it."

        elif " bug" in playerText and "eat " in playerText:
            if "bug" in rooms[currentRoom][0] or  "bug" in bag:
                print "This is a special kind of bug.\nI won't eat it."
            else:
                print "Hmm... I can't find it."

        elif " painting" in playerText and "eat " in playerText:
            if "painting" in rooms[currentRoom][0] or  "painting" in bag:
                print "This is a wall painting.\nIs it even possible to eat?"
            else:
                print "Hmm... I can't find it."

        elif " shovle" in playerText and "eat " in playerText:
            if "shovle" in rooms[currentRoom][0] or  "shovle" in bag:
                print "Do you think with your butt?\nFor your information,\nthat was a retorical question."
            else:
                print "Hmm... I can't find it."
        elif " egg" in playerText and "eat " in playerText:
            if "egg" in bag or rooms[currentRoom][0]:
                print "You eat the eggs."
                if "egg" in bag:
                    bag.remove("egg")
                elif "egg" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("egg")
            else:
                print "NO! The eggs is gone."
                
        elif " sword" in playerText and "eat " in playerText:
            if "sword" in bag or rooms[currentRoom][0]:
                print "You eat the sword and it cuts you in half."
                print "You recieve a Darwin award and die."
                die()
            else:
                print "NO! The sword could not be found."
                
        elif "hidden door" in playerText and "eat " in playerText:
            if "hidden door" in bag or rooms[currentRoom][0]:
                print "You cannot find your fork, so you cannt eat the hidden door. Maybe the fork is also hidden... behind the door? :o"
            else:
                print "NO! The hidden door is gone."
                
        elif " rope" in playerText and "eat " in playerText:
            if "rope" in bag or "rope" in rooms[currentRoom][0]:
                print "You eat the rope, and it's the best rope you have ever tasted."
                print "You get stomach ache"
                if "rope" in bag:
                    bag.remove("rope")
                elif "rope" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("rope")
            else:
                print "NOOO! it is gone."
                
        elif "eat bag" == playerText or "eat the bag" == playerText:
            print("Well, that isn't smart!")
            print("The bag realize what you are about to do,")
            print("and eats you instead.")
            newEgg("eat bag")
            die()
        elif " torch" in playerText and "eat " in playerText:
            if "torch" in bag:
                print "You eat the torch and realize your mistake."
                print "You're not able to explore. You walk home again"
                bag.remove("torch")
                die()
            elif "torch" in hand or "torch" in rooms[currentRoom][0]:
                print "You eat the torch and realize your mistake."
                print "You're not able to explore. You walk home again"
                if "torch" in bag:
                    bag.remove("torch")
                elif "torch" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("torch")
                print("\n")
                die() 
            else:
                print("You have to find the torch first")
                
        elif " vine" in playerText and "eat " in playerText:
            if "vine" in rooms[currentRoom][0] or  "vine" in bag:
                print "Nom, nom, nom. This was tasty.\nBut it's plenty left."
            else:
                print "Hmm... I can't find it."
                
        elif " sphinx" in playerText and "eat " in playerText:
            if "sphinx" in rooms[currentRoom][0] or  "sphinx" in bag:
                print "The sphinx comes alive and eats you."
                die()
            else:
                print "Hmm... I can't find it."
                
        elif "easter egg" in playerText and "eat " in playerText:
            if len(easterEggsFound) > 0:
                print "You lost a easter egg"
                easterEggsFound.remove(easterEggsFound[-1])
            else:
                print "You have no easter egg left."
        
        elif " sand" in playerText and "eat " in playerText and len(playerText.split()) <= 2:
            if "sand" in bag or "sand" in rooms[currentRoom][0]:
                print "No way!"+bcolors.OKBLUE +" Do you see how much it is?"
                choice = raw_input("\n> " + bcolors.ENDC)
                choice = choice.lower()
                if "yes" in choice or "y" in choice:
                    print "No you don't"
                    newEgg("liar")
                elif "no" in choice:
                    print "So don't you tell me to eat it all"
                else:
                    print "That's not a response i expected."
            else:
                print "You can't seem to find any sand."
        
        elif " pyramid" in playerText and "eat " in playerText:
            if ("pyramid" in bag or "pyramid" in rooms[currentRoom][0]) and ("pyramid" in lastInput and "eat" in lastInput):
                print "Derp, It would ruin the game."
                print "And I said \"Don't you tell me to do it again\""
            elif ("pyramid" in bag or "pyramid" in rooms[currentRoom][0]) and ("pyramid" not in lastInput or "eat" not in lastInput):
                print "Do you have no brain? It's fucking huge."
                print "Don't you tell me to do it again"
            else:
                print "You can't find the pyramid"
                
        elif " gate" in playerText and "eat " in playerText:
           if "gate" in bag or "gate" in rooms[currentRoom][0]:
                print "The gate is made of stone"
                print "I don't eat stone"
           else:
                print "This is not the gate you're looking for."
                newEgg("droid")
                
        elif " skeleton" in playerText and "eat " in playerText:
           if "skeleton" in bag or "skeleton" in rooms[currentRoom][0]:
                print "Well this is just to dry."
                print "But if you say so"
                if "skeleton" in bag:
                    bag.remove("skeleton")
                elif "skeleton" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("skeleton")
           else:
                print "Hmm... I can't find it."
                
        elif ("spider web" in playerText or "web" in playerText) and "eat " in playerText:
           if "spider web" in bag or "spider web" in rooms[currentRoom][0]:
                print "Hmm... like bubble gum."
                print "I'm going to sell this when i get home"
                if "spider web" in bag:
                    bag.remove("spider web")
                elif "spider web" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("spider web")
           else:
                print "Hmm... I can't find it."
                
        elif " slime" in playerText and "eat " in playerText:
           if  "slime" in rooms[currentRoom][0]:
                print "I can't get the slime of my hands"
                print "it is to sticky. I'll just rubbit of in the bag"
                bag.append("slime")
           elif "slime" in bag:
                print "I can't get it up from the bag"
                print "Luckily it's in a separate pocket "
           else:
                print "Hmm... I can't find it."
                
        elif " web" not in playerText and "giant spder" in playerText and "eat " in playerText or ("spider" in playerText and "eat " in playerText):
            if  "giant spider" in rooms[currentRoom][0]:
                print "I think it would eat me instead"
                unavalibleMove = True
            elif "giant spider" in bag:
                print "Nom, nom nom"
                print "I'll save some for later"
            else:
                print "Hmm... I can't find it."
        
        elif "mummy" in playerText and "eat " in playerText:
            if  "mummy" in rooms[currentRoom][0]:
                print "I think it would eat me instead"
                unavalibleMove = True
            elif "mummy" in bag:
                print "No! Just No!"
                print "You set the mummy free again\n to avoid beeing forced to eat it."
            else:
                print "Hmm... I can't find it."
        
        elif " cinnamon" in playerText and "eat " in playerText:
            if "spices" in rooms[currentRoom][0] or  "spices" in bag:
                print "cinnamon challange accepted!"
                print "You tried and FAILED!"
                newEgg("cinnamon")
            else:
                print "Hmm... I can't find it."
        
        elif " statue" in playerText and "eat " in playerText:
            if "statue" in rooms[currentRoom][0] or  "statue" in bag:
                print "Nope! What you are suggesting is ill-adviced"
            else:
                print "Hmm... I can't find it."
        
        elif "drink " in playerText and " potion" in playerText:
            if ("potion" in rooms[currentRoom][0] or  "potion" in bag):
                print "You starts to feel weird, your sight gets blurry and you find it hard to keep track of directions"
                
                #Need a variable that keeps track i toxicated, if toxicated it should be a little bit harder to play the game. Not toxicated if drinks from the fountain
                toxicated = True
                
                if "potion" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("potion")
                elif "potion" in bag:
                    bag.remove("potion")
                rooms[currentRoom][0].append("glass bottle")
            else:
                print "Hmm... I can't find it."
        
        elif "find " in playerText and " sword" in playerText:
                print "How one usaly go about to find something, is by looking around. How ever in this case you might need to inspect some objects to find it."

        elif ("put on " in playerText and " ring" in playerText) or ("use " in playerText and " ring" in playerText and len(playerText.split()) == 2):
            if "ring" in rooms[currentRoom][0] or  "ring" in bag:
                print "You have now put on the ring. You suddenly realise the ring is very precious to you! You are also slightly transparent and overwhelmed with a desire to rule them all!"
            else:
                print "Hmm... I can't find it."

        elif "give cactus to " in playerText and " statue" in playerText:
            if "statue" in rooms[currentRoom][0] or  "statue" in bag:
                print "You gave your cactus to the statue! The statue now looks ridicoulsish"
            else:
                print "Hmm... I can't find it."

        elif "dance " in playerText and " skeleton" in playerText:
            if "skeleton" in rooms[currentRoom][0] or  "skeleton" in bag:
                print "The skeleton wakes up and does the boogey-woogey with you! You feel weird dancing with the dead..."
            else:
                print "Hmm... I can't find it."

        elif "pet " in playerText and " skeleton" in playerText:
            if "skeleton" in rooms[currentRoom][0] or  "skeleton" in bag:
                print "You pet the skeleton nicely. It purrs and starts dancing weirdly"
            else:
                print "Hmm... I can't find it."

        elif "mellon " in playerText and " mysterious door" in playerText:
            if "mysterious door" in rooms[currentRoom][0] or  "mysterious door" in bag:
                print "You hear gandalf from the other side \"YOOOU SHALL NOT PAAAASS!\""
                newEgg("gandalf")
            else:
                print "Hmm... I can't find it."

        elif "give cake " in playerText and " skeleton" in playerText:
            if "skeleton" in rooms[currentRoom][0] or  "skeleton" in bag:
                print "Skeletons don't eat this kind of cake you fool"
            else:
                print "Hmm... I can't find it."

        elif ":d" == playerText:
                print "YAY! :D :D :D :D :D :D :D =P"

        elif "poke " in playerText and " cactus" in playerText:
            if "cactus" in rooms[currentRoom][0] or  "cactus" in bag:
                print "You poke the cactus. It turns out that that was not such a good idea. Your finger hurts a little bit now. "
            else:
                print "Hmm... I can't find it."

        elif "drink " in playerText and " cactus" in playerText:
            if "cactus" in rooms[currentRoom][0] or  "cactus" in bag:
                print "You open up the cactus and drink some of its juice. Very tasty!"
            else:
                print "Hmm... I can't find it."

        elif "sit " in playerText and " birds nest" in playerText:
            if "birds nest" in rooms[currentRoom][0] or  "birds nest" in bag:
                print "You sit in the birds nest and pretend that you're an egg. A birds swoops down and feeds you chewed worms. You feel nourished!"
                rooms[currentRoom][0].append("bird")
            else:
                print "Hmm... I can't find it."

        elif "pet " in playerText and " weird old man" in playerText:
            if "weird old man" in rooms[currentRoom][0] or  "weird old man" in bag:
                print "The weird old man starts to pur."
            else:
                print "Hmm... I can't find it."

        elif "search " in playerText and " spider web" in playerText:
            if "spider web" in rooms[currentRoom][0] or  "spider web" in bag:
                print "Internet connection not found. Try to go outside."
            else:
                print "Hmm... I can't find it."

        elif "dive " in playerText and " fountain" in playerText:
            if "fountain" in rooms[currentRoom][0] or  "fountain" in bag:
                print "There seems to be an entire city at the bottom of this fountain. It must be bigger on the inside. To bad you can't hold your breath any longer. You return to the surface. "
            else:
                print "Hmm... I can't find it."

        elif "how do you do?" == playerText:
                print "I'm well, thank you. And you?\nYou don't have to answer, you're playing this game. Obviosly everything is nice "

        elif "tickle " in playerText and " weird old man" in playerText:
            if "weird old man" in rooms[currentRoom][0] or  "weird old man" in bag:
                print "The weird old man gives you a creepy smile."
            else:
                print "Hmm... I can't find it."

        elif "talk " in playerText and " duck" in playerText:
            if "duck" in rooms[currentRoom][0] or  "duck" in bag:
                print "You talk to the rubber duck and figure out what you did wrong at your latest exam."
            else:
                print "Hmm... I can't find it."

        elif "hi" == playerText:
            print "You greet the world and the wolrd wishes you a nice day."

        elif "what can i do" in playerText or "what can i do?" in playerText:
            print "That's upp to you my friend. But I would suggest to explore the pyramid"

        elif "explore pyramid" == playerText or "explore the pyramid" == playerText:
            print "You have to be more describing ^^"

        elif "be more describing" == playerText:
            print "Well fock off m8! You know what I mean."

        elif "knock on " in playerText and " gate" in playerText:
            if "gate" in rooms[currentRoom][0] or  "gate" in bag:
                print "There seems to be nobuddy home."
            else:
                print "Hmm... I can't find it."

        elif "engulf " in playerText and " smell" in playerText:
            if "smell" in rooms[currentRoom][0] or  "smell" in bag:
                print "The smell is confused. How can a human engulf smell."
            else:
                print "Hmm... I can't find it."
        
        elif "take" in playerText and "nose" in playerText:
            if "swinx" in rooms[currentRoom][0]:
                global takenNose
                print "HaHa, got your nose!"
                if takenNose == False:                   
                    bag.append("nose")
                    takenNose = True
                newEgg("got nose")
            else:
                print "Hmm... I can't find it."
                
        elif "see how much sand it is" in playerText:
            if "sand" in rooms[currentRoom][0]:
                print "By pure intuition, you deduce that there are 69105 grains of sand in this loosely defined subset of the desert."
            else:
                print "Hmm... I can't find it."

        elif "praise the sun" in playerText:
                print "\"Praise the Sun and Jolly Cooperation!\""

        elif "surf" in playerText and "web" in playerText:
            if "spider web" in rooms[currentRoom][0] or  "spider web" in bag:
                print "Finally you can update your Facebook status."
            else:
                print "Hmm... I can't find it."

        elif "burn" in playerText and "web" in playerText:
            if "web spider" in rooms[currentRoom][0] or  "web spider" in bag:
                print "Only the ashes remain."
                if "spider web" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("spider web"); rooms[currentRoom][0].append("ash")
                elif "spider web" in bag:
                    bag.remove("spider web"); bag.append("ash")
            else:
                print "Hmm... I can't find it."

        elif "knock on door" in playerText:
                print "What door? Please be more specific."

        elif "harvest " in playerText and " cactus" in playerText:
            if "cactus" in rooms[currentRoom][0] or  "cactus" in bag:
                print "You harvested cactus fruits. They seem delicious"
                bag.append("cactus fruits")
            else:
                print "Hmm... I can't find it."

        elif "walk" == playerText:
                print "You take a strol and end up where you started"

        elif "head " in playerText and " baskets" in playerText:
            if "baskets" in rooms[currentRoom][0] or  "baskets" in bag:
                print "You put a basket on your head and use it as a epic hat."
                newEgg("nice hat")
            else:
                print "Hmm... I can't find it."

        elif "scream " in playerText and " ghost" in playerText:
            if "ghost" in rooms[currentRoom][0] or  "ghost" in bag:
                print "You scream loudly!!!! It sounds something like  AAARRRHHHAAAHII!!! The ghost seems most pleased with itself. The ghost awards you a extra cake!"
                bag.append("cake")
            else:
                print "Hmm... I can't find it."

        elif ("flirt " in playerText or "seduce " in playerText) and " ghost" in playerText:
            if "ghost" in rooms[currentRoom][0] or  "ghost" in bag:
                print "You start showing of some epic moves to impress the ghost but you quckly stop when you recognise who the ghost is(or maybe used to be). It turns out it is you late greatgreatgreat grandma and you have now aroused her. She awards you with a special ancestral ring!"
                if "ring" not in bag and "ring" not in rooms[currentRoom][0]:
                    bag.append("ring")
            else:
                print "Hmm... I can't find it."
        
        elif "see how much it is" in playerText and "eat sand" ==lastInput:
            if "sand" in rooms[currentRoom][0]:
                print "By pure intuition, you deduce that there are 69105 grains of sand in this loosely defined subset of the desert."
            else:
                print "Hmm... I can't find it."
                
        elif "peace" in playerText and "hostile super sand castle" in playerText:
            if "hostile super sand castle" in rooms[currentRoom][0] or  "hostile super sand castle" in bag:
                print "Your enemies do not trust you. But they are willing to concede to a peacy treaty if you supply them with mudcake.", bcolors.OKBLU,"Do you accept?"
                choice = raw_input("\n> " + bcolors.ENDC)
                choice = choice.lower()
                if "yes" in choice or "y" in choice:
                    if "mudcake" in rooms[currentRoom][0] or  "mudcake" in bag:
                        print "Okey,  deal."
                        rooms[currentRoom][0].append("fortified sand castle")
                        if "mudcake" in rooms[currentRoom][0]:
                            rooms[currentRoom][0].remove("mudcake")
                        elif "mudcake" in bag:
                            bag.remove("mudcake")
                    else:
                        print "You have no mudcake!"
                elif "no" in choice:
                    print "You are weird"
                else:
                    print "That's not a response I expected"
            else:
                print "Hmm... I can't find it."
    
        elif "peace" in playerText and "hostile fortified sand castle" in playerText:
            if "hostile fortified sand castle" in rooms[currentRoom][0] or  "hostile fortified sand castle" in bag:
                print "Your enemies are highly suspious of you, but they agree to accept a peace treaty in return for a cake.", bcolors.OKBLU,"Do you accept?"
                choice = raw_input("\n> " + bcolors.ENDC)
                choice = choice.lower()
                if "yes" in choice or "y" in choice:
                    if "cake" in rooms[currentRoom][0] or  "cake" in bag:
                        print "Okey,  deal."
                        rooms[currentRoom][0].append("fortified sand castle")
                        if "cake" in rooms[currentRoom][0]:
                            rooms[currentRoom][0].remove("cake")
                        elif "cake" in bag:
                            bag.remove("cake")
                    else:
                        print "You have no cake!"
                elif "no" in choice:
                    print "You are weird"
                else:
                    print "That's not a response I expected"
            else:
                print "Hmm... I can't find it."
                
        elif "talk" in playerText and "weird old man" in playerText and timesTalkedWeirdMan == 0:
            if "weird old man" in rooms[currentRoom][0] or  "weird old man" in bag:
                print "Hrumpf! To someone with such few colours on them, I will not speak! Buggrit, millenium hand and shrimp! Colours of the rainbow, are needed to be worthy!"
            else:
                print "Hmm... I can't find it."

        elif "talk" in playerText and "weird old man" in playerText and timesTalkedWeirdMan == 1:
            if "weird old man" in rooms[currentRoom][0] or  "weird old man" in bag:
                print "The weird old man stares in awe at your rainbow-coloured hand. \"Blessed by the rainbow, your hand has been! Most marvelous, this is. To the source of this blessing, bring me!\""
                timesTalkedWeirdMan = 2
            else:
                print "Hmm... I can't find it."
        
        elif "talk" in playerText and "weird old man" in playerText and timesTalkedWeirdMan == 2:
            if "weird old man" in rooms[currentRoom][0] or  "weird old man" in bag:
                print "\"Waited I have. Present me the sorurce of blessing you will.\""
            else:
                print "Hmm... I can't find it."

        elif ("present " in playerText or "show " in playerText or "reveal " in playerText or "bring " in playerText) and "nyan cat" in playerText:
            if ("weird old man" in rooms[currentRoom][0] or  "weird old man" in bag) and ("nyan cat" in rooms[currentRoom][0] or  "nyan cat" in bag):
                if timesTalkedWeirdMan == 2:
                    print "You introduce the weird old man to nyan cat (Nyan cat says \"NYAN\"). The weird old man looks really excited. \"So the source of the blessing, this is. Extraordinary, this is!\" He jumps around in circles happily. "
                    timesTalkedWeirdMan = 3
                elif timesTalkedWeirdMan <= 2:
                    print "The weird old man shies away from you, he doesn't trust you enought. \"What are you trying to do? Asked for this, I have not!\""
            else:
                print "Hmm... I can't find it."

        elif "talk" in playerText and "weird old man" in playerText and (timesTalkedWeirdMan == 3 or "nyan cat" in rooms[currentRoom][0]):
            if "weird old man" in rooms[currentRoom][0] or  "weird old man" in bag:
                print "The weird old man is now feeling very grateful towards you. \"For this noble mission, rewarded with two gifts you shall be!\" The weird old man pulls off one of his dirty old socks and throws it in your face. It smells horrendous. \"This practical sock, the first gift is!\" The old man seems to think that this was a really generous gift. \"Knowledge, the second gift is. Know this: in the prescence of certain pointy buildings, help can be summoned with the aid of this ancient incantation 'general add'. Heard, I have, that these summoned creatures can be used together with castles of sand.\""
                newEgg("dobby")
                if "smelly sock" not in rooms[currentRoom][0] and  "smelly sock" not in bag:
                    bag.append("smelly sock")
            else:
                print "Hmm... I can't find it."

       
        
        elif "knock" in playerText and "mysterious door" in playerText:
            if "mysterious door" in rooms[currentRoom][0] or  "mysterious door" in bag:
                print "You knock on the mysterious door. After a short pause interval of time reply is heard:", bcolors.OKBLUE ,"\"Who's there?"
                choice = raw_input("\n> " + bcolors.ENDC)
                choice = choice.lower()
                print  bcolors.OKBLUE, choice, "who?"
                choice = raw_input("\n> " + bcolors.ENDC)
                print "Make sense this does not! Understand I don't\" The mysterious door swings open and a weird old man appears. The door swings shut behind him."
                rooms[currentRoom][0].append("weird old man")
                if "mysterious door" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("mysterious door")
                    rooms[currentRoom][0].append("strange door")
                elif "mysterious door" in bag:
                    bag.remove("mysterious door")
                    bag.append("strange door")
            else:
                print "Hmm... I can't find it."
        
        
        
        elif "reverse" in playerText and "sand" in playerText:
            if "sand" in rooms[currentRoom][0] or  "sand" in bag:
                print "You have reversed sand"
                if "sand" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("sand")
                    rooms[currentRoom][0].append("dnas")
                elif "sand" in bag:
                    bag.remove("sand")
                    bag.append("dnas")
            else:
                print "Hmm... I can't find it."

        elif "promote" in playerText and "super general" in playerText:
            if "super general" in rooms[currentRoom][0] or  "super general" in bag:
                print "The super general is promoted to a supreme general"
                if "super general" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("super general")
                    rooms[currentRoom][0].append("supreme general")
                elif "super general" in bag:
                    bag.remove("super general")
                    bag.append("supreme general")
            else:
                print "Hmm... I can't find it."

        elif "promote" in playerText and "supreme general" in playerText:
            if "supreme general" in rooms[currentRoom][0] or  "supreme general" in bag:
                print "The supreme general is now general relativity"
                if "supreme general" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("supreme general")
                    rooms[currentRoom][0].append("general relativity")
                elif "supreme general" in bag:
                    bag.remove("supreme general")
                    bag.append("general relativity")
            else:
                print "Hmm... I can't find it."

        elif "promote" in playerText and "general relativity" in playerText:
            if "general relativity" in rooms[currentRoom][0] or  "general relativity" in bag:
                print "General relativity is now a shogun"
                if "general relativity" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("general relativity")
                    rooms[currentRoom][0].append("shogun")
                elif "general relativity" in bag:
                    bag.remove("general relativity")
                    bag.append("shogun")
            else:
                print "Hmm... I can't find it."

        elif "promote" in playerText and "shogun" in playerText:
            if "shogun" in rooms[currentRoom][0] or  "shogun" in bag:
                print "Hurray! The shogun is promoted to a kitty master."
                if "shogun" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("shogun")
                    rooms[currentRoom][0].append("kitty master")
                elif "shogun" in bag:
                    bag.remove("shogun")
                    bag.append("kitty master")
            else:
                print "Hmm... I can't find it."

        elif "declare war" in playerText and "fortified sand castle" in playerText:
            if "fortified sand castle" in rooms[currentRoom][0] or  "fortified sand castle" in bag:
                print "You declare war upon the fortified sand castle. It is now a hostile fortified sand castle. The garrison inside throws rocks at you from a distance."
                if "fortified sand castle" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("fortified sand castle")
                    rooms[currentRoom][0].append("hostile fortified sand castle")
                elif "fortified sand castle" in bag:
                    bag.remove("fortified sand castle") 
                    bag.append("hostile fortified sand castle")
            else:
                print "Hmm... I can't find it."


        elif "give " in playerText and " jonathan" in playerText and "smelly sock" in playerText:
            if("jonathan" in rooms[currentRoom][0] or "jonathan" in bag) and ("smelly sock" in rooms[currentRoom][0] or "smelly sock" in bag):
                print "\"There are times when a gentleman has to be courageous and fight, even when his opponent is bigger than he is and he knows he's going to lose! With this hamoninfused smelly sock I shall defeat Dio! Oh, but wait a minute. Someone has to be the designated poser by the bizarre door. Could you take over for me, Joseph?\" An even more fabulous person arrives, and stands in the doorway with a mischievous grin on his face, and an inhumane pose on his body. "
                rooms[currentRoom][0].append("joseph")
                if "jonathan" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("jonathan")
                elif "jonathan" in bag:
                    bag.remove("jonathan")
                if "smelly sock" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("smelly sock")
                elif "smelly sock" in bag:
                    bag.remove("smelly sock")
            else:
                print "Hmm... I can't find it."
                
        

        elif "poke " in playerText and " jonathan" in playerText:
            if("jonathan" in rooms[currentRoom][0] or "jonathan" in bag):
                print "\"That was not very gentemanly of you!\" He looks very shocked. "
            else:
                print "Hmm... I can't find it."





        elif "declare war" in playerText and "super sand castle" in playerText:
            if "super sand castle" in rooms[currentRoom][0] or  "super sand castle" in bag:
                print "You declare war upon the super sand castle. The super general vows to end your life. The castle is now a hostile super sand castle."
                if "super sand castle" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("super sand castle")
                    rooms[currentRoom][0].append("hostile super sand castle")
                elif "super sand castle" in bag:
                    bag.remove("super sand castle")
                    bag.append("hostile super sand castle")
            else:
                print "Hmm... I can't find it."
            
            
            
            
        elif "open" in playerText and "mysterious door" in playerText:
            if "mysterious door" in rooms[currentRoom][0] or  "mysterious door" in bag:
                print "The door appears to be locked. You hear movements from the other side. I wonder if it is possible to get whatever it is on the other side to open the door..."
            else:
                print "Hmm... I can't find it."
        
        elif "promote" in playerText and "general" in playerText:
            if "general" in rooms[currentRoom][0] or  "general" in bag:
                print "The general is promoted to a super general"
                if "general" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("general"); rooms[currentRoom][0].append("super general")
                elif "general" in bag:
                    bag.remove("general"); bag.append("super general")
            else:
                print "Hmm... I can't find it."

        elif "talk" in playerText and "mysterious door" in playerText:
            if "mysterious door" in rooms[currentRoom][0] or  "mysterious door" in bag:
                print "You say \"Hello?\". The sounds of movements from the other side are silenced. Suddenly you hear a hoarse voice coming from the other side: \"Knock on doors, polite people do\""
            else:
                print "Hmm... I can't find it."
                
        elif "fry" in playerText and "egg" in playerText:
            if "egg" in rooms[currentRoom][0] or  "egg" in bag:
                print "You've made an omelet."
                if "egg" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("egg"); rooms[currentRoom][0].append("omelet")
                elif "egg" in bag:
                    bag.remove("egg"); bag.append("omelet")
            else:
                print "Hmm... I can't find it."
                
        elif "poke" in playerText and "mysterious door" in playerText:
            if "mysterious door" in rooms[currentRoom][0] or  "mysterious door" in bag:
                print "It's not very effective."
            else:
                print "Hmm... I can't find it."
                
        elif "reverse" in playerText and "sand" in playerText:
            if "sand" in rooms[currentRoom][0] or  "sand" in bag:
                print "You have reversed sand"
                if "sand" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("sand"); rooms[currentRoom][0].append("dnas")
                elif "sand" in bag:
                    bag.remove("sand"); bag.append("dnas")
            else:
                print "Hmm... I can't find it."
        
        elif "talk" in playerText and "kitty master" in playerText:
            if "kitty master" in rooms[currentRoom][0] or  "kitty master" in bag:
                print "You speak at length with the very wise kitty master. You are rewarded with awesome arcane knowledge about kittens. "
            else:
                print "Hmm... I can't find it."

        elif "talk" in playerText and "shogun" in playerText:
            if "shogun" in rooms[currentRoom][0] or  "shogun" in bag:
                print "The shogun is to busy looking awesome to talk to people like you. "
            else:
                print "Hmm... I can't find it."

        elif "talk" in playerText and "super general" in playerText:
            if "super general" in rooms[currentRoom][0] or  "super general" in bag:
                print "The super generals mustache vibrates in a fascinating way during your conversation. It's a bit distracting. After the discussion you realize that you don't remember anything about it except for the hypnotic movement of the mustache. "
            else:
                print "Hmm... I can't find it."

        elif "talk" in playerText and "supreme general" in playerText:
            if "supreme general" in rooms[currentRoom][0] or  "supreme general" in bag:
                print "The mustache of the supreme general moves around in big, gracious movements. It is truly a sight to behold. After a while into the conversation you realize that the supreme general is not actually speaking to you, but is simply moving around the mustache in a way that communicates with you on some deeper level. You learn many things about life, the universe, and everything. "
            else:
                print "Hmm... I can't find it."

        elif "poke" in playerText and "super general" in playerText:
            if "super general" in rooms[currentRoom][0] or  "super general" in bag:
                print "The super general gets super angry!"
            else:
                print "Hmm... I can't find it."

        elif "poke" in playerText and "supreme general" in playerText:
            if "supreme general" in rooms[currentRoom][0] or  "supreme general" in bag:
                print "Your finger almost gets stuck in the supreme generals mustache!"
            else:
                print "Hmm... I can't find it."

        elif "poke" in playerText and "kitty master" in playerText:
            if "kitty master" in rooms[currentRoom][0] or  "kitty master" in bag:
                print "You consider poking the kitty master. But then you remember that kittens are awesome and cute, and you do not wish to annoy the kitty master. "
            else:
                print "Hmm... I can't find it."
        
        elif "poke" in playerText and "shogun" in playerText:
            if "shogun" in rooms[currentRoom][0] or  "shogun" in bag:
                print "The shogun cuts off your finger. This is not good. But the shogun thinks that you have learned your lesson and puts back your finger using tape. "
            else:
                print "Hmm... I can't find it."
                
        elif "enter" in playerText and "hostile fortified sand castle" in playerText:
            if "hostile fortified sand castle" in rooms[currentRoom][0] or  "hostile fortified sand castle" in bag:
                print "The guards on duty will not let you in. They throw rocks at you from a distance. "
            else:
                print "Hmm... I can't find it."

        elif "enter" in playerText and "fortified sand castle" in playerText:
            if "fortified sand castle" in rooms[currentRoom][0] or  "fortified sand castle" in bag:
                print "You are hailed at the gates of the fortified sand castle by two guards on duty. You are allowed to walk around inside the castle walls. The castle is quite impressing, considering that it is made of sand. "
            else:
                print "Hmm... I can't find it."
        
        elif "enter" in playerText and "hostile super sand castle" in playerText:
            if "hostile super sand castle" in rooms[currentRoom][0] or  "hostile super sand castle" in bag:
                print "You are not allowed to enter. The guards shoot arrows at you, you barely manages to duck. You run away from the castle. "
            else:
                print "Hmm... I can't find it."

        elif "enter" in playerText and "super sand castle" in playerText:
            if "super sand castle" in rooms[currentRoom][0] or  "super sand castle" in bag:
                print "You are hailed at the gates by the guards on duty. You are allowed to enter the castle. You walk around inside the walls. You are impressed by how much these people have achieved using only sand. The craftmanship is really good, somehow the castle manages to be both beautiful and still be easy to defend. "
            else:
                print "Hmm... I can't find it."
                
        elif "open" in playerText and "strange door" in playerText:
            if "strange door" in rooms[currentRoom][0] or  "strange door" in bag:
                print "THe door is once again locked. You do not hear any motion from the other side. "
            else:
                print "Hmm... I can't find it."

        elif "poke" in playerText and "strange door" in playerText:
            if "strange door" in rooms[currentRoom][0] or  "strange door" in bag:
                print "Strangely enough this does not have any effect. "
            else:
                print "Hmm... I can't find it."
        
        elif "talk" in playerText and "bug" in playerText:
            if "bug" in rooms[currentRoom][0] or  "bug" in bag:
                print "Go away! Yer buggin' me!"
            else:
                print "Hmm... I can't find it."
        
        elif "talk" in playerText and "strange door" in playerText:
            if "strange door" in rooms[currentRoom][0] or  "strange door" in bag:
                print "There is no response"
            else:
                print "Hmm... I can't find it."
                
        elif "knock" in playerText and "strange door" in playerText:
            if "strange door" in rooms[currentRoom][0] or  "strange door" in bag:
                print "Nothing interesting happens"
            else:
                print "Hmm... I can't find it."

        elif "bug" in playerText and "statue" in playerText:
            if "statue" in rooms[currentRoom][0] or  "statue" in bag:
                print "The bug annoys the statue. The statue punches the bug. The bug loses 1 hp."
            else:
                print "Hmm... I can't find it."

        elif "poke" in playerText and "painting" in playerText:
            if "painting" in rooms[currentRoom][0] or  "painting" in bag:
                print "Mona Lisa pokes back."
            else:
                print "Hmm... I can't find it."
                
        elif "open" in playerText and "hidendoor" in playerText:
            if "hidendoor" in rooms[currentRoom][0] or  "hidendoor" in bag:
                print "You can't open the hidden door since it hidden =P"
            else:
                print "Hmm... I can't find it."
        
        elif "ride" in playerText and "bug" in playerText:
            if "bug" in rooms[currentRoom][0] or  "bug" in bag:
                print "You climb onto the bug and ride it for a while."
            else:
                print "Hmm... I can't find it."

        elif "knock down" in playerText and "general" in playerText:
            if "general" in rooms[currentRoom][0] or  "general" in bag:
                print "You give the general a mighty push. He looks surprised, and rolls down the pyramid, down into oblivion."
            else:
                print "Hmm... I can't find it."

        elif "push" in playerText and "general" in playerText:
            if "general" in rooms[currentRoom][0] or  "general" in bag:
                print "You push the general. He flies horisontally away from the pyramid. He just keeps accelerating indefinetly. You think you hear a faint \"Team general flies away again...\" *sparkle*"
                if "general" in bag:
                    bag.remove("general")
                elif "general" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("general")
            else:
                print "Hmm... I can't find it."

        elif "talk" in playerText and "ghost" in playerText:
            if "ghost" in rooms[currentRoom][0] or  "ghost" in bag:
                print "BOOOO! I'm the scariest ghost there is! There is nothing in this world which isn't afraid of me, and nothing which I fear!"
            else:
                print "Hmm... I can't find it."

        elif "poke" in playerText and "ghost" in playerText:
            if "ghost" in rooms[currentRoom][0] or  "ghost" in bag:
                print "Your finger goes straigt through the ghost. "
            else:
                print "Hmm... I can't find it."

        elif "poke" in playerText and "nyan cat" in playerText:
            if "nyan cat" in rooms[currentRoom][0] or  "nyan cat" in bag:
                print "The cat says \"NYAN NYAN\". Rainbowness intensifies."
            else:
                print "Hmm... I can't find it."

        elif "poke" in playerText and "big cat" in playerText:
            if "big cat" in rooms[currentRoom][0] or  "big cat" in bag:
                print "The big cat playfully bites you finger. At least, that's how it looks from the cats perspective. From your perspective, your finger is now bleeding a lot."
            else:
                print "Hmm... I can't find it."

        elif "sphinx" in playerText and "poke" in playerText:
            if "sphinx" in rooms[currentRoom][0] or  "sphinx" in bag:
                print "The sphinx springs to life and hits you, and the returns to being a statue. You become paralyzed for a short while"
                time.sleep(5)
            else:
                print "Hmm... I can't find it."
        
        elif "anger" in playerText and "ra" in playerText:
            if "ra" in rooms[currentRoom][0] or  "ra" in bag:
                print "Ra is not pleased with you"
            else:
                print "Hmm... I can't find it."

        elif "dig" in playerText and "sand" in playerText:
            if "sand" in rooms[currentRoom][0] or  "sand" in bag:
                print "You dig the sand, puting the sand you dig up in a hole that seems to appear where your digging."
            else:
                print "Hmm... I can't find it."

        elif "lick" in playerText and "cake" in playerText:
            if "cake" in rooms[currentRoom][0] or  "cake" in bag:
                print "The cake is now yours."
            else:
                print "Hmm... I can't find it."

        elif "taste " in playerText and " cake" in playerText:
            if "cake" in rooms[currentRoom][0] or  "cake" in bag:
                print "You taste the cake. It tastes like a rainbow on fire!"
            else:
                print "Hmm... I can't find it."

        elif "cut" in playerText and "cake" in playerText:
            if ("cake" in rooms[currentRoom][0] or  "cake" in bag) and ("sword" in bag or "sword" in rooms[currentRoom][0]):
                print "You use the sword to cut the cake into several pieces."
            else:
                print "Hmm... I can't find both sword and cake."
        
        elif "hide" in playerText and "hidden door" in playerText:
            if "hidden door" in rooms[currentRoom][0] or  "hidden door" in bag:
                print "The hidden door is now extreamly hidden and happy."
                rooms[currentRoom][0].remove("hidden door")
                newEgg("gone")
            else:
                print "Hmm... I can't find it."

        elif "improve" in playerText and "cake" in playerText:
            if ("cake" in rooms[currentRoom][0] or  "cake" in bag) and ("spices" in rooms[currentRoom][0] or  "spices" in bag):
                print "You add the spices to the cake. It is now a much better cake, it might attract ghouls."
            else:
                print "Hmm... I can't find the spices."

        elif "discomode" in playerText or "disco mode" in playerText:
                print "The discomode is broken. Instead you feel unhappy =("

        elif "knock down" in playerText and "gate" in playerText:
            if "gate" in rooms[currentRoom][0] or  "gate" in bag:
                print "The gate knocks you back."
            else:
                print "Hmm... I can't find it."

        elif "smell" in playerText and "spices" in playerText:
            if "spices" in rooms[currentRoom][0] or  "spices" in bag:
                print "The spices smell... spicy!"
            else:
                print "Hmm... I can't find it."

        elif "poke" in playerText and "slime" in playerText:
            if "slime" in rooms[currentRoom][0] or  "slime" in bag:
                print "It wiggles ominously..."
            else:
                print "Hmm... I can't find it."

        elif "skeleton" in playerText and "talk" in playerText:
            if "skeleton" in rooms[currentRoom][0] or  "skeleton" in bag:
                print "\"If you keep going the way you are now... you're gonna have a bad time.\""
            else:
                print "Hmm... I can't find it."

        elif "find hidden" in playerText and "hidden door" not in playerText:
                print "You will have to find all the hidden things for your self."
         
        elif "what is love" in playerText:
            print "Baby don't hurt me."
        
        elif "dance" == playerText:
            print "You feel wierd dancing alone."
           
        elif "dig" in playerText and ("shovle" in playerText or "hole" in playerText):
            if "shovle" in rooms[currentRoom][0] or  "shovle" in bag:
                print "The floor is made of stone.\nYou ruined the shovle."
                if "shovle" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("shovle")
                else:
                    bag.remove("shovle")
            else:
                print "Hmm... I can't find the shovle."

        elif "find" in playerText and "treasure" in playerText:
                print "You will have to do that yourself."
            
        elif "light bag" in playerText:
                print "If I did that i would have a hard time carying my items."

        elif "leave pyramid" in playerText and ableToLeave == False:
                print "How are you supposed to manage that? the gate is closed.\nAnd since there is a curse you can't open it from the inside."

        elif "open gate" in playerText and currentRoom != 0 and ableToLeave == False:
                print "You can't open the gate from the inside."

        elif "read code" in playerText:
                print "I was thinking of putting half of my code here, but that's not a smart thing to do. So I'll just give you a easter egg. And if you really want to read code, here it is: \"CODE\""
                newEgg("code")

        elif "talk" in playerText and "statue" in playerText:
            if "statue" in rooms[currentRoom][0] or  "statue" in bag:
                print "Statue replies: \"Sorry! I'm not allowed to talk in this game.\""
            else:
                print "Hmm... I can't find it."

        elif "burn" in playerText and ("monster" in playerText or "mummy" in playerText or "giant spider" in playerText or "spider" in playerText):
            if "mummy" in playerText and "mummy" in rooms[currentRoom][0]:
                print "Congrats! you killed the mummy"
                print "the curse is now lifted and you can return home from your expedition."
                ableToLeave = True
                rooms[currentRoom][0].remove("mummy")
            elif "spider" in playerText and "giant spider" in rooms[currentRoom][0]:
                print "Congrats! you killed the giant spider"
                rooms[currentRoom][0].remove("giant spider")
            elif "monster" in playerText and ("mummy" in rooms[currentRoom][0] or "giant spider" in rooms[currentRoom][0]):
                    if "mummy" in rooms[currentRoom][0]:
                        print "Congrats! you killed the mummy"
                        print "the curse is now lifted and you can return home from your expedition."
                        ableToLeave = True
                        rooms[currentRoom][0].remove("mummy")
                    elif "giant spider" in rooms[currentRoom][0]:
                        print "Congrats! you killed the giant spider"
                        rooms[currentRoom][0].remove("giant spider")
            else:
                print "Hmm... I can't find it."

        elif "read" in playerText and ("scroll" in playerText or "pergament" in playerText):
            if "pergament scroll" in rooms[currentRoom][0] or  "pergament scroll" in bag:
                print "- Too cure the Blackconfusion one must drink the healing water\n- The mummy will arise when the god of death is rightfully bribed"
            else:
                print "Hmm... I can't find it."

        elif ("buy" in playerText or "treasure" in playerText) and "spider web" in playerText:
            if "spider web" in rooms[currentRoom][0] or  "spider web" in bag:
                print "A spider crawls out from the web and offers you a spider donut. It costs treasure.", bcolors.OKBLUE,"Do you want it?"
                choice = raw_input("\n> " + bcolors.ENDC)
                choice = choice.lower()
                if "yes" in choice or "y" in choice:
                    if "treasure" in rooms[currentRoom][0] or  "treasure" in bag:
                        print "Okey, thank you for trading."
                        rooms[currentRoom][0].append("spider donut")
                        if "treasure" in rooms[currentRoom][0]:
                            rooms[currentRoom][0].remove("treasure")
                        else:
                            bag.remove("treasure")
                    else:
                        print "You have no treasure!"
                    
                elif "no" in choice:
                    print "Okey! bye!"
                else:
                    print "That's not a response i expected."
            else:
                print "Hmm... I can't find it."
       
        elif ("talk" in playerText or "riddle" in playerText) and "sphinx" in playerText:
            if "sphinx" in rooms[currentRoom][0] or  "sphinx" in bag:
                number = int(22*random.random())
                #print number
                
                print "The sphinx presents you with a riddle\n\"", riddle[number], "\""
            else:
                print "Hmm... I can't find it."
        elif "wiggle" in playerText and "slime" in playerText:
            if "slime" in rooms[currentRoom][0] or  "slime" in bag:
                print "It wiggles back seductively."
            else:
                print "Hmm... I can't find it."

        elif "talk" in playerText and "thot" in playerText:
            if "thot" in rooms[currentRoom][0] or  "thot" in bag:
                print "u feel nerdier."
            else:
                print "Hmm... I can't find it."
                
        elif "talk" in playerText and "ra" in playerText:
            if "ra" in rooms[currentRoom][0] or  "ra" in bag:
                print "You open upp your inner heart to Ra and tell the god how you would lik Ra to lighten up you day.\nYou feel disapointed that teh stone statue dos not answer"
            else:
                print "Hmm... I can't find it."

        elif "equip " in playerText and " sword"  in playerText:
            print "no need to equip it if I have it in my bag. I'm verry fast with this things you see. Just tell me what to kill and I'll do my best."
            unavalibleMove = True

        elif "find chuck norris" == playerText:
           print "Chuck Norris is dead :(, E's not pinin! E's passed on! This Norris is no more! He has ceased to be! 'E's expired and gone to meet his maker!"
           newEgg("Chuck Norris")

        elif "\"help\"" == playerText:
            print "Oh, my!!\n Really, reeeaaally. Nooooo nooooope. I'm not gonna give you this one. try again."

        elif "general add" in playerText:
            if "pyramid" in rooms[currentRoom][0] or  "pyramid" in bag:
                print "Suddenly, there is a general sitting on top of the pyramid. He waves happily towards you."
                rooms[currentRoom][0].append("general")
                newEgg("general")
            else:
                print "Hmm... I can't find it."

        elif "talk" in playerText and "programmer" in playerText:
                print "\"Why are you talking to me when you could be playing my game instead? :D\""
           
        elif "poke" in playerText and "programmer" in playerText:
                print "\"Hey, stop that! If you don't behave I might patch you away\""
            
        elif "speak" in playerText and "programmer" in playerText:
                print "\"Did you know that there is something called easter eggs in this game? Gotta hatch 'em all ;)\""
            
        elif "kill" in playerText and "programmer" in playerText:
                print "The programmer is not pleased. You are now considered a malicious virus. And such things must be cleansed. You do not have the right to remain silent, but you have the right to remain dead!!! SMITE!"
                die()

        elif "pet" in playerText and "programmer" in playerText:
                print "The programmer purrs happily."
            
        elif "sleep" in playerText and "sarcophagus" in playerText:
            if "sarcophagus" in rooms[currentRoom][0] or  "sarcophagus" in bag:
                if sarcophagusOpen == True:
                    print "You lay down and take a nap in the sarcophagus. You sleep soundly You feel well rested."
                else:
                    print "You need to open it first."
            else:
                print "Hmm... I can't find it."

        elif "flirt" in playerText and "grumpy cat" in playerText:
            if "grumpy cat" in rooms[currentRoom][0] or  "grumpy cat" in bag:
                print "The grumpy cat is not interested. You respect its boundaries. "
            else:
                print "Hmm... I can't find it."

        elif "pet" in playerText and "grumpy cat" in playerText:
            if "grumpy cat" in rooms[currentRoom][0] or  "grumpy cat" in bag:
                print "You pet the grumpy cat. It does not look pleased *grumpiness intensifies*"
            else:
                print "Hmm... I can't find it."

        elif "talk" in playerText and "nyan cat" in playerText:
            if "nyan cat" in rooms[currentRoom][0] or  "nyan cat" in bag:
                print "\"NYAN!\""
            else:
                print "Hmm... I can't find it."

        elif "talk" in playerText and "big cat" in playerText:
            if "big cat" in rooms[currentRoom][0] or  "big cat" in bag:
                print "\"I ONLY SPEAK USING BIG LETTERS\""
            else:
                print "Hmm... I can't find it."

        elif "climb" in playerText and "vine" in playerText:
            if "vine" in rooms[currentRoom][0] or  "vine" in bag:
                print "You climb up the vine. You feel like you're quite high up right now. But you cannot see your house from here. Because your indoors. :P"
            else:
                print "Hmm... I can't find it."

        elif "talk" in playerText and "hidden door" in playerText:
            if "hidden door" in rooms[currentRoom][0] or  "hidden door" in bag:
                print "Why are you trying to talk to a door? Especially one you cannot find"
            else:
                print "Hmm... I can't find it."

        elif "pasta" in playerText and "skeleton" in playerText:
            if "skeleton" in rooms[currentRoom][0] or  "skeleton" in bag:
                print "\"Nyeh Heh Heh!\""
            else:
                print "Hmm... I can't find it."
        
        elif ("build" in playerText or "make" in playerText) and "sand" in playerText and ("castle" in playerText or "tower" in playerText):
            if "sand" in rooms[currentRoom][0] or  "sand" in bag:
                print "You build a beautiful sand castle. It looks very epic. :)"
                rooms[currentRoom][0].append("sand castle")
            else:
                print "Hmm... I can't find it."
        
        elif ("swim" in playerText or "bathe" in playerText) and "fountain" in playerText:
            if "fountain" in rooms[currentRoom][0] or  "fountain" in bag:
                print "You splash around in the fountain. It's quite fun and invigorating. It almost feels as if you are somehow younger than before..."
            else:
                print "Hmm... I can't find it."

        elif "swim" in playerText and "treasure" in playerText:
            if "treasure" in rooms[currentRoom][0] or  "treasure" in bag:
                print "You dive into the treasure and splash around. You feel like Scrouge Mcduck, except you don't feel like a duck. Ok, there might also be other ways in which you are not like Scrooge McDuck, but you know what I mean."
                newEgg("scrooge McDuck")
            else:
                print "Hmm... I can't find it."

        elif "expfys" in playerText and "thot" in playerText:
            if "thot" in rooms[currentRoom][0] or  "thot" in bag:
                print "Thot helps you finish your expfys. This makes you very happy"
            else:
                print "Hmm... I can't find it."

        elif ("pray " in playerText or "whorship " in playerText) and " ra" in playerText:
            if "ra" in rooms[currentRoom][0] or  "ra" in bag:
                print "You whisper a silent prayer to the sun god. For a brief moment the room is filled with shining, bright light. "
            else:
                print "Hmm... I can't find it."

        elif ("pray " in playerText or "whorship " in playerText) and " anubis" in playerText:
            if "anubis" in rooms[currentRoom][0] or  "anubis" in bag:
                print "You pray to anubis. The god of the dead ressurects someone! A ghost appears..."
                rooms[currentRoom][0].append("ghost")
                newEgg("ghost")
            else:
                print "Hmm... I can't find it."

        elif ("pray " in playerText or "whorship " in playerText) and " thot" in playerText:
            if "thot" in rooms[currentRoom][0] or  "thot" in bag:
                print "You are filled with knowledge. Specifically, you now know more about how that fluffy stuff that appears in your navel appears. "
            else:
                print "Hmm... I can't find it."

        elif "scare" in playerText and "ghost" in playerText:
            if "ghost" in rooms[currentRoom][0] or  "ghost" in bag:
                print "You sneak up on the ghost and shout \"Booh!\". The ghost looks really frightened. "
            else:
                print "Hmm... I can't find it."

        elif ("pray " in playerText or "whorship ") and "osiris" in playerText:
            if "osiris" in rooms[currentRoom][0] or  "osiris" in bag:
                print "You direct a prayer to Osiris. Nothing appears to have happened.... at least not yet.."
            else:
                print "Hmm... I can't find it."

        elif "find" in playerText and "hidden door" in playerText:
            if "hidden door" in rooms[currentRoom][0] or  "hidden door" in bag:
                print "You cannot find the hidden door. But it finds you..."
            else:
                print "Hmm... I can't find it."

        elif "pet " in playerText and "big cat" in playerText:
            if "big cat" in rooms[currentRoom][0] or  "big cat" in bag:
                print "You approach the big cat to pet it. It looks curiously at you. Suddenly it springs on top of you. The big cat is now petting you. You purr softly. "
            else:
                print "Hmm... I can't find it."

        elif "joke" in playerText and "skeleton" in playerText:
            if "skeleton" in rooms[currentRoom][0] or  "skeleton" in bag:
                print "You tell the skeleton a joke. Suddenly the skeleton comes alive, and seems to want share one of its jokes with you \"You may think that I'm lazy since I'm normally just standing around here, being dead, but I've actually been doing a ton. A skele-ton!\" *badum tsh* You have now learned the skeleton pun."
                bag.append("skeleton pun")
            else:
                print "Hmm... I can't find it."

        elif "joke" in playerText and "grumpy cat" in playerText:
            if "grumpy cat" in rooms[currentRoom][0] or  "grumpy cat" in bag:
                print "You tell the grumpy cat a joke, hoping that this will cheer it up. The cat stares at you with intense grumpiness. It's hollow laugh echos throughout the room. The laughter is sarcastic, and is sucking away all joy from it's surroundings. The grumpy cat remains grumpy. You feel silly."
            else:
                print "Hmm... I can't find it."

        elif "poke" in playerText and "grumpy cat" in playerText:
            if "grumpy cat" in rooms[currentRoom][0] or  "grumpy cat" in bag:
                print "The cat looks at you with despairing, grumpy eyes. Stoopid hooman, leave me aloon. "
            else:
                print "Hmm... I can't find it."

        elif "pet" in playerText and "nyan cat" in playerText:
            if "nyan cat" in rooms[currentRoom][0] or  "nyan cat" in bag:
                print "The cat purrs softly. Suddenly light bursts forth from the cat, rainbow coloured light. The whole room is filled with rainbows. Your perception of reality has been expanded. You look down at the hand you used to pet the cat with, it is now rainbow coloured. That is very cool, but you might still want to get that checked out by a doctor or something."
                timesTalkedWeirdMan = 1
            else:
                print "Hmm... I can't find it."

        elif "smell " in playerText:
            if "smell" in rooms[currentRoom][0] or  "smell" in bag:
                print "You smelled the smell"
                if "smell" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("smell")
                elif "smell" in bag:
                    bag.remove("smell")
            else:
                print "Hmm... I can't find it."
        
        elif "fart" in playerText and "general" in playerText:
            if "general" in rooms[currentRoom][0] or  "general" in bag:
                print "You fart in the general direction of the general"
            else:
                print "Hmm... I can't find it."

        elif "talk" in playerText and "general" in playerText:
            if "general" in rooms[currentRoom][0] or  "general" in bag:
                print "Arrrgh mateys! I be bad at following appropriate stereotypes"
            else:
                print "Hmm... I can't find it."
        
        elif "demote " in playerText and " general" in playerText:
            if("general" in rooms[currentRoom][0] or "general" in bag):
                print "The general is demoted to an admiral."
                rooms[currentRoom][0].append("admiral")
                if "general" in rooms[currentRoom][0]:
                    rooms[currentRoom][0].remove("general")
                elif "general" in bag:
                    bag.remove("general")
            else:
                print "Hmm... I can't find it."
        
        elif "poke" in playerText and "general" in playerText:
            if "general" in rooms[currentRoom][0] or  "general" in bag:
                print "The general orders you to not do that."
            else:
                print "Hmm... I can't find it."
                
        
        elif investigate(playerText) and " admiral" in playerText:
            if("admiral" in rooms[currentRoom][0] or "admiral" in bag):
                print "The admiral has an admirable mustache. I mean, it's not as good as the one the general had. Still pretty good though"
            else:
                print "Hmm... I can't find it."
        
        elif "speak " in playerText:
            print "You might wanna try \"talk\" instead of \"speak\""
        
        elif "talk" in playerText and "sand" in playerText:
            if "sand" in rooms[currentRoom][0] or  "sand" in bag:
                print "I must avenge Oberyn myself. The sand can't walk away and becomes angry."
            else:
                print "Hmm... I can't find it."
        
        elif "pet" in playerText or "stroke" in playerText or "scratch belly" in playerText:
            print "There is no time to pet such things."
            print "Lets explore!"
        
        else:
            return False
        return True
        
       
    
    #This is supposed to run first
    def first(playerText):
        global currentRoom
        global lastRoom
        global faceDirection
        global unavalibleMove
        global torchLit
        
        if "how to" in playerText:
            print("Well... It's not rocket science. Duh!")
            return True
        elif ("don't panic" == playerText or "dont panic" == playerText) and monsterInRoom():
            unavalibleMove = True
            newEgg("42")
            print "For a moment, nothing happened. Then, after a second or so, nothing continued to happen. The monster is very confused that you're not panicing. You two start a conversation and clear things up. The monster apologies for not already have killed you and tells you that it will soon try again"
            
        elif "don't" in playerText or "can't" in playerText or "can't" in playerText or "dont" in playerText or "can not" in playerText or "do not" in playerText:
            print("Well... Don't tell me what I shouldn't do.")
            print("Tell me what I shall do")
            return True
        elif len(playerText)> 50:
            print("Can you say that again? i don't remember it all :P")
            return True
        elif "feedback" == playerText:
            feedback()
            return True
        elif "high score" in playerText or "highscore" in playerText:
            return highScore()
        elif "open" in playerText and "bag" in playerText or "bag" == playerText.split()[0] or "check gear" in playerText:
            print 'You have: ' '%s' % ', '.join(map(str, bag))
            unavalibleMove = True
            return True
        elif "cheat" in playerText.split():
            bag.append(" ".join(playerText.split()[1:]))
            return True
        elif "sudo" in playerText.split():
            raw_input(bcolors.FAIL + "Password >> "+ bcolors.ENDC)
            print "Wrong password."
            newEgg("sudo")
            return True
        elif "pick up" in playerText or "take" in playerText.split() or "t" == playerText.split()[0]:
            return pickUp(playerText)
        elif "drop" in playerText.split() or "d" == playerText.split()[0]:
            return drop(playerText)
        elif "music" in playerText.split():
            if musicMode == "on":
                unavalibleMove = True
                return music(playerText)
            else:
                print "Music is off. Sorry you ned the right fils and change the mode at the very top of the script"
        elif "attack" in playerText.split() or "kill" in playerText.split() or "eliminate" in playerText.split() or ("sword" in playerText and ("giant spider" in playerText or "spider" in playerText or "mummy" in playerText or "monster" in playerText)):
            return kill(playerText)
        elif special(playerText):
                return True
        else:
            return False
        
    return first(playerText)
        
def enterRoom():
    global rooms
    global currentRoom
    global torchLit
    global faceDirection
    global lastInput
    global unavalibleMove
    global listAt
    global toxicated
    MonsterRedyToAttack = False
    
    
    if torchLit == False:
        print("You entered a dark room.")
    else:
        if torchLit == True:
            if toxicated and int(2*random.random()) == 1:
                print "You can see that there is things in this room, however you can't recollect what these things are called"
            else:
                print("You are in a room with %i doors"% len(rooms[currentRoom][1]))
                doorFacing(faceDirection)
            
                print 'You see: ' '%s' % ', '.join(map(str, rooms[currentRoom][0]))
    listAt = "room"
    
    
    
    
    
    stay = True
    
    while stay == True: 
        print " \n"
        goback = False
        
        unavalibleMove = False
        if monsterInRoom():
            MonsterRedyToAttack = True
            print "Caution! The monster is running towards you, and will kill you if you don't act smart.\n"
            if musicMode == "on":
                music("stop")
                music3.play()
                currentMusic = music3
        choice = raw_input("> ")
        if len(choice) == 0:
            continue
        choice = choice.lower()
        
        #If ther is a digit comand
        numbers = re.findall(r'\d+', choice)

        if toxicated:
            faceDirection = int(4*random.random())
            if "talk" in choice:
                print "All you can manage is some strange words \"banjaxed fleein, loo brota\""
                newEgg("banjaxed")
                continue
            if int(4*random.random()) == 1:
                print "\"How could anyone eaven do that, it seems to be impossible\" You think for your self."
                continue

        if ("open" in lastInput and "bag" in lastInput or "bag" == lastInput.split()[0] or "check gear" in lastInput):
            listAt = "bag"
        elif "look" == choice or "look around" in choice or "search" in choice or "s" == choice and  ("inventory" and "bag" and "at") not in choice or "ls" == choice:
            listAt = "room"

        if len(numbers) > 0:
            for x in range(0, len(numbers)):
                if listAt == "bag" and int(numbers[x]) <= len(bag) and int(numbers[x]) != 0: 
                    choice = choice + " " + bag[int(numbers[x])-1]
                elif listAt == "room" and int(numbers[x]) <= len(rooms[currentRoom][0]) and int(numbers[x]) != 0:
                    choice = choice + " " + rooms[currentRoom][0][int(numbers[x])-1]
                else:
                    goback = True
                    print "One of your numbers were too big or too small"
                    break
        
        #return to top of whhile loop
        if goback:
            continue
        
        
        #Chek what the input matches.
        if always(choice):
            print " "
        elif "look" == choice or "look around" in choice or "search" in choice or "s" == choice and  ("inventory" and "bag" and "at") not in choice or "ls" == choice:
            if torchLit == True:
                if toxicated and int(2*random.random()) == 1:
                    print "You can see that there is things in this room, however you can't recollect what these things are called"
                else:
                    print("You are in a room with %i doors"% len(rooms[currentRoom][1]))
                    doorFacing(faceDirection)
                
                    print 'You see: ' '%s' % ', '.join(map(str, rooms[currentRoom][0]))
            else:
                print("You can't see a rats arse.")
                print("Maybe you don't give a rats arse about that.")
        elif "give a rats arse" in choice:
            print("Well, how unpredictable")
        else:
            print "That command is unknown to me! Try something else."
            unavalibleMove = True
            with open('failedCommands.txt', 'a') as txt:
                txt.write('\n\n' + choice + ",         CURRENTROOM: " + str(currentRoom) + ",     Last input: " + lastInput)
        
       
       ##If you did not kill the monster it will kill you
        if monsterInRoom() and unavalibleMove == False and MonsterRedyToAttack == True:
            if "giant spider" in rooms[currentRoom][0]:
                print "The giant spider bites your head of!"
            else:
                print "The mummy huggs you untill you starv to death."
            die()    
        else:
            MonsterRedyToAttack = False
        lastInput = choice

def start():
    global currentRoom
    if musicMode == "on":
        global music1
    global lastInput
    global listAt
    gate = "closed"
    
    print " \n \n \n \n \n"
    print(" ----------------------------------------------------\n")
    print("|   Welcome to a text adventure created by R2D2*     |")
    print("|                   Version: 2.3                     |")
    print("|        Want usefull commands? Type: \"help\"         |")
    print("|                                                    |")
    print("|              *With help from Bjorn                 |")
    print("\n ----------------------------------------------------")
    print " \n \n \n"
    print "You are in front of an ancient pyramid,"
    print "prepared for an expedition."
    print "What do you do?"
    
    
    if musicMode == "on":
        music1.play()
        currentMusic = music1
    
    stay = True
    while stay == True:
        print " \n"
        goback = False
        
        
        choice = raw_input("> ")
        if len(choice) == 0:
            continue
        choice = choice.lower()
        
        
        #If ther is a digit comand
        numbers = re.findall(r'\d+', choice)

        if ("open" in lastInput and "bag" in lastInput or "bag" == lastInput.split()[0] or "check gear" in lastInput):
            listAt = "bag"
        elif "look" == choice or "look around" in choice or "search" in choice or "s" == choice and  ("inventory" and "bag" and "at") not in choice or "ls" == choice:
            listAt = "room"

        if len(numbers) > 0:
            for x in range(0, len(numbers)):
                if listAt == "bag" and int(numbers[x]) <= len(bag) and int(numbers[x]) != 0: 
                    choice = choice + " " + bag[int(numbers[x])-1]
                elif listAt == "room" and int(numbers[x]) <= len(rooms[currentRoom][0]) and int(numbers[x]) != 0:
                    choice = choice + " " + rooms[currentRoom][0][int(numbers[x])-1]
                else:
                    goback = True
                    print "One of your numbers were too big or too small"
                    break
        
        if goback:
            continue
        
        
        if always(choice):
            print " "
        elif "look" == choice or "look around" in choice or "search" in choice or "s" == choice and  ("inventory" and "bag" and "at") not in choice or "ls" == choice:   
            if  "pyramid" in rooms[currentRoom][0]:
                if gate == "open":
                    print "you find a open gate to the pyramid."
                else:
                    print "you find a closed gate to the pyramid."
                
                print 'You see: ' '%s' % ', '.join(map(str, rooms[currentRoom][0]))
            else:
                print "Hmm... You can't see the pyramid,"
                print "and your bag feels heavy."
        elif "open" in choice and ("gate" in choice or "door"in choice):
            if "pyramid" in rooms[currentRoom][0]:
                if gate != "open": 
                    print "The gate slides open and a nasty smell engulfs you."
                elif gate == "open":
                    print "The gate is already opened"
                gate = "open"
                if "smell" not in rooms[currentRoom][0] and "smell" not in bag:
                    rooms[currentRoom][0].append("smell")
            else:
                print "You can't open the gate when the pyramid is in your bag."
                
        
        elif "close" in choice and ("gate" in choice or "door" in choice):
            if "pyramid" in rooms[currentRoom][0]:
                if gate != "open": 
                    print "The gate havn't been opened yet."
                elif gate == "open":
                    print "No! I came here to explore."
            else:
                print "You can't close the gate when the pyramid is in your bag."
        
        
        elif "enter" == choice or "enter forward door" in choice or "forward" in choice or "enter door" in choice or "enter gate" in choice or "enter pyramid" in choice or "f" == choice or "forward" in choice or "walk in" in choice or "go inside" in choice:
            if gate == "open":
                print "You enter the pyramid and the gate closes behind you. An ancient curse makes it impossible to open the closed gate again. You now need to find a way to lift the curse, so you can return home."
                print " "
                stay = False
                currentRoom = 1
                enterRoom()
            else:
                print "You need to open the gate first"
        elif "cd pyramid" == choice:
            print "You enter the pyramid and the gate closes behind you. An ancient curse makes it impossible to open the closed gate again. You now need to find a way to lift the curse, so you can return home."
            print " "
            stay = False
            currentRoom = 1
            enterRoom()
        else:
            print "That command is unknown to me! Try something else."
            unavalibleMove = True
            with open('failedCommands.txt', 'a') as txt:
                txt.write('\n\n' + choice + ",         CURRENTROOM: " + str(currentRoom) + ",     Last input: " + lastInput)
        lastInput = choice


start()
