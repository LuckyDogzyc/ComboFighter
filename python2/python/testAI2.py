import sys
from py4j.java_gateway import get_field
import os
from ComboMaker import ComboMaker
import json
import time


class testAI2(object):
################### init ########################
    def __init__(self, gateway):
        self.gateway = gateway

        #init Params
        self.popSize = 10

        # init Actions
        self.actions = []
        self.records = {}
        self.ends = {}
        self.type = {}

        # grab or generate map of combos
        if os.path.exists("testCombo.json"):
            self.cm = ComboMaker(False)
        else:
            self.cm = ComboMaker(True)
        
        # keys used to traverse directories
        self.x = ['close', 'mid', 'far']
        self.y = ['ground', 'mid', 'apex']
        self.e = ['none', 'little', 'some', 'lot']


##################### close #####################
    def close(self):
        with open("testCombos.json", 'w') as file:
            json.dump(self.cm.combos, file)
        pass
    
####################### processing ##################
    def processing(self):
        # Just compute the input for the current frame
        if self.frameData.getEmptyFlag() or self.frameData.getRemainingFramesNumber() <= 0:
            self.isGameJustStarted = True
            return
        if not self.isGameJustStarted:
            pass
        else:
            # this "else" is going to be called in the first frame in the round
            self.isGameJustStarted = False
            self.currentRoundNum = self.frameData.getRound()
            print(self.currentRoundNum)
            #print("Round:", self.currentRoundNum)

        frame = self.frameData.getFramesNumber()

        #if there are more inputs to execute a skill, this moves to the next input
        if self.cc.getSkillFlag():
            self.inputKey = self.cc.getSkillKey()
            return


        #empty the input
        self.inputKey.empty()
        self.cc.skillCancel()
        

        #if there is no combo string currently, get a combo string
        if len(self.actions) == 0:
            print('Getting new combo string')
            
            #Determine the state
            xdist = ""
            ydist = ""
            energy = ""
            
            #initialize records if first time
            if str(self.currentRoundNum) not in self.records:
                self.records[str(self.currentRoundNum)] = []
                self.type[str(self.currentRoundNum)] = []

            #Store the beginning time of the combo string
            self.records[str(self.currentRoundNum)].append(frame)
            
            #Determine x distance
            if(self.frameData.getDistanceX() <= 200):
                xdist = self.x[0]
            elif(self.frameData.getDistanceX() <= 400):
                xdist = self.x[1]
            else:
                xdist = self.x[2]
            
            #Determine y distance
            if(self.frameData.getDistanceY() <= 50):
                ydist = self.y[0]
            elif(self.frameData.getDistanceY() <= 150):
                ydist = self.y[1]
            else:
                ydist = self.y[2]
            
            #Determine energy amount
            if(self.frameData.getCharacter(self.player).getEnergy() <= 10):
                energy = self.e[0]
            elif(self.frameData.getCharacter(self.player).getEnergy() <= 50):
                energy = self.e[1]
            elif(self.frameData.getCharacter(self.player).getEnergy() <= 100):
                energy = self.e[2]
            else:
                energy = self.e[3]
            
            #Store which combo string was used
            self.type[str(self.currentRoundNum)].append(str(xdist + ":" + ydist + ":" + energy))
            
            #Set list of actions
            self.actions = self.cm.combos['stored'][xdist][ydist][energy]
        
        if len(self.actions) > 0 and self.frameData.getFramesNumber() > 1 and self.frameData.getRemainingFramesNumber() > 16:
            # Execute the next input in the combo string
            if(self.actions[0] == "N"): # 'do nothing' action
                pass
            else:
                self.cc.commandCall(self.actions[0])
            self.actions = self.actions[1:]
        
        #Store the ending time of the combo string
        if not self.actions:
            if str(self.currentRoundNum) not in self.ends:
                self.ends[str(self.currentRoundNum)] = []
            
            self.ends[str(self.currentRoundNum)].append(frame)
        
        
        pass

#################### roundEnd ###################
        # please define this method when you use FightingICE version 3.20 or later
    def roundEnd(self, x, y, z):

        #print(x)
        print(-y)
        #print(z)
        print("\nRound End")
        
        self.actions = []
                        
        with open("Outputs\\records.txt", 'r') as file:
            data = file.read().splitlines(True)
            
            print("Calculating")
            #iterate through each line in records.txt
            for i in range(len(data)):
                #iterate through each completed combo
                for j in range(len(self.ends[str(i+1)])):
                    #Store the beginning and end of the combo, and the combo used
                    beginning = self.records[str(i+1)][j]
                    ending = self.ends[str(i+1)][j]
                    type = self.type[str(i+1)][j].split(":")
                    
                    
                    #Get the segment of records.txt for this combo
                    newRecord = data[i][beginning:ending]
                    
                    #Calculate fitness
                    fitness = self.cm.calcFitness(newRecord)
                    
                    #Set the best combo as the saved one
                    if self.cm.combos['old'][type[0]][type[1]][type[2]]:
                        if self.cm.combos['vFit'][type[0]][type[1]][type[2]] < fitness:
                            self.cm.combos['vFit'][type[0]][type[1]][type[2]] = fitness
                            self.cm.combos['old'][type[0]][type[1]][type[2]] = self.cm.combos['stored'][type[0]][type[1]][type[2]]
                    else:
                        self.cm.combos['vFit'][type[0]][type[1]][type[2]] = fitness
                        self.cm.combos['old'][type[0]][type[1]][type[2]] = self.cm.combos['stored'][type[0]][type[1]][type[2]]
                        
                    print(self.cm.combos['vFit'][type[0]][type[1]][type[2]])
                    
                    #Determine the probabilities to use
                    if type[0] == 'far':
                        flag = False
                    else:
                        flag = True
                    
                    #Generate the Child
                    self.cm.combos['stored'][type[0]][type[1]][type[2]] = self.cm.mutate(self.cm.combos['old'][type[0]][type[1]][type[2]], flag)

        #Do this every popSize amount of rounds
        if self.currentRoundNum % self.popSize == 0:
            print('Grabbing Combos')
            #Store all the stored combo strings and their fitness
            current = []
            for i in self.x:
                for j in self.y:
                    for k in self.e:
                        current.append([str(self.cm.combos['vFit'][i][j][k]), i, j, k])
            
            print('Sorting Combos')
            #Sort the list 
            current = self.cm.mergeSort(current)
            
            print('Storing top 10 combos of this round')
            current = current[:10]
            self.cm.combos['top'][str(self.currentRoundNum)] = current
            
            print('Storing to json file')
            with open("testCombos.json", 'w') as file:
                json.dump(self.cm.combos, file)

        pass

#################################################
############ Not Changing These #################
#################################################

#################### getInformation #############
    def getInformation(self, frameData, isControl):
        # Getting the frame data of the current frame
        self.frameData = frameData
        self.cc.setFrameData(self.frameData, self.player)

####################### getScreenData ##################
    # please define this method when you use FightingICE version 4.00 or later
    def getScreenData(self, sd):
        pass

####################### initialize #####################
    def initialize(self, gameData, player):
        # Initializng the command center, the simulator and some other things
        self.inputKey = self.gateway.jvm.struct.Key()
        self.frameData = self.gateway.jvm.struct.FrameData()
        self.cc = self.gateway.jvm.aiinterface.CommandCenter()

        self.player = player
        self.gameData = gameData
        self.simulator = self.gameData.getSimulator()

        return 0

####################### input #######################
    def input(self):
        # Return the input for the current frame
        return self.inputKey

    # This part is mandatory
    class Java:
        implements = ["aiinterface.AIInterface"]

