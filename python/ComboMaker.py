import random
import numpy
import json

class ComboMaker(object):

###################### Make Combo ###########################
# This method randomly generates a combo string
#############################################################
    def makeCombo(self):
        combo = ""
        for i in range(self.cLength):
            combo += numpy.random.choice(self.inputs, p=self.close)
        
        return combo

###################### Init Function ########################
# This method initializes the ComboMaker object
#
# It will create two dictionaries to store combo strings and
#  their fitness values and populate the combo string
#  dictionary with randomly generated combo strings
#
#                   # Variables #
# self.combos will store a multidimensional dictionary of
#  combo strings. 
# self.combos['vFit'] will store a multidimensional dictionary of
#  fitness values for combo strings in the same position in
#  self.combos.
# self.inputs holds an array of characters representing
#  possible inputs to execute
# self.close and self.far hold an array of percentage
#  chances for each input to be picked when creating/mutating
#  a combo string
# self.cLength an integer for the length of strings generated
# xdist, ydist, and energy are the keys that will be used to
#  store the combo strings in the dictionaries.
##############################################################
    def __init__(self, flag):
        #The dictionaries that the combo strings and their fitness values will be stored in
        if flag == True:
            self.combos = {}
            self.combos['stored'] = {}
            self.combos['vFit'] = {}
            self.combos['old'] = {}

        
            #The inputs and their probabilites
            self.inputs = ['U','D','L','R','A','B','C','N'] #possible inputs
            self.close = [0.1, 0.1, 0.1, 0.1, 0.2, 0.2, 0.1, 0.1] #chance of inputs up close
            self.far = [0.2, 0.1, 0.1, 0.2, 0.1, 0.1, 0.1, 0.1] #chance of inputs far away
            
            #The length of the combo strings created/mutated
            self.cLength = 1000
            
            #The keys that will direct to a combo string
            xdist = ['close', 'mid', 'far']
            ydist = ['ground', 'mid', 'apex']
            energy = ['none', 'little', 'some', 'lot']
            
            #Create the multidimensional dictionaries holding the combo strings
            for i in xdist:
                self.combos['stored'][str(i)] = {}
                self.combos['vFit'][str(i)] = {}
                self.combos['old'][str(i)] = {}
                
                for j in ydist:
                    self.combos['stored'][str(i)][str(j)] = {}
                    self.combos['vFit'][str(i)][str(j)] = {}
                    self.combos['old'][str(i)][str(j)] = {}
                    
                    for k in energy:
                        self.combos['stored'][str(i)][str(j)][str(k)] = self.makeCombo()
                        self.combos['vFit'][str(i)][str(j)][str(k)] = 0
                        self.combos['old'][str(i)][str(j)][str(k)] = ""
                    
        else:
            with open("testCombos.json", 'r') as file:
                self.combos = json.load(file)
        
###################### Mutate ###############################
# This method takes a combo string and a boolean value and
# creates a new mutated combo string
#
# The boolean value determines which set of input probabilites
# are used
############################################################
    def mutate(self, parent, flag):
        child = ""
        
        if flag == True:
            iList = self.close
        else:
            iList = self.far
        
        for i in range(len(parent)):
            r = random.random()
            if r < 0.1:
                child += numpy.random.choice(self.inputs, p=iList)
            else:
                child += parent[i]
        
        return child

###################### Calc Fitness #########################
# This method uses a string of '1's and '0's to calculate
# the fitness of a combo string. '1's mean that the test
# dummy was stunned for that frame. '0's mean that the test
# dummy was not stunned for that frame. 
#
# To calculate fitness, it finds the longest amount of frames
# the enemy was stunned for. It then finds the immediate left
# combo string and divides its length by the space between 
# it and the longest combo. It does the same for the right 
# side and then adds the length of the longest combo to the
# two calculated numbers
#############################################################
    def calcFitness(self, record):
        biggest = 0
        biggestStart = 0
        tempStart = 0
        tempBegin = True
        biggestEnd = 0
        isBiggest = False
        count = 0

        countHit = 0

        isConnect = False

        # Find the biggest string of '1's
        for j in range(len(record)):
            if record[j] == '1':
                countHit += 1
                isConnect = True
                # If starting a new line of '1's
                # remember the beginning
                if tempBegin == True:
                    tempBegin = False
                    tempStart = j

                count += 1

                # If bigger than biggest, remember the
                # information of the biggest
                if count > biggest:
                    isBiggest = True
                    biggest = count
                    biggestStart = tempStart


            else:
                if isConnect:
                    isConnect = False
                    count += 1
                else:

                    count = 0
                    tempBegin = True

                    # If this was the biggest, remember the end
                    if isBiggest == True:
                        isBiggest = False
                        biggestEnd = j - 1




        # If the last character was part of the biggest string
        # make sure biggestEnd is set
        if isBiggest == True:
            biggestEnd = len(record)


        # Get the left and right combos and space
        left = 0
        lSpace = 0
        right = 0
        rSpace = 0
        flag = False

        # Finds the combo to the left
        biggestStart -= 1
        while biggestStart >= 0:
            # Found the left combo, counting it
            if record[biggestStart] == '1':
                flag = True
                left += 1

            # If found the left combo, leave
            # else count the space between combos
            else:
                if flag == True:
                    break
                lSpace += 1

            biggestStart -= 1

        flag = False
        # finds the combo to the right
        biggestEnd += 1
        while biggestEnd < len(record):
            # Found the right combo, counting it
            if record[biggestEnd] == '1':
                flag = True
                right += 1

            # If found the right combo, leave
            # else count the space between combos
            else:
                if flag == True:
                    break
                rSpace += 1

            biggestEnd += 1
        
        #Set space to 0 if there is nothing to the left/right
        if left == 0:
            lSpace = 0
        if right == 0:
            rSpace = 0

        # Calculate Fitness of combo
        div = 1
        lheur = (left/div)/((1+lSpace)**2)
        rheur = (right/div)/((1+rSpace)**2)
        fitness = lheur+rheur+biggest/div
        
        return fitness