import sys
from py4j.java_gateway import get_field
import os
import json
import ComboMaker


class GeneticAI(object):
    #################################
    # The functions we change #######
    #################################
    
    ############# Init Function ##############
    def __init__(self, gateway):
        self.gateway = gateway

        #init Params
        self.popSize = 10

        # init Actions
        self.actions = ""
        self.records = []

        self.inputLen = 0

        try:
            file = open('combos.json', 'r')
        except FileNotFoundError:
            self.mp = ComboMaker()
        else:
            self.mp = json.load(file)
            file.close()
    
    #################### Round End ##########################
        # please define this method when you use FightingICE version 3.20 or later
    def roundEnd(self, x, y, z):
        #print("endGeneticAI1")
        print(-x)
        #print(-y)
        #print(z)

        #Read new actions
        if(self.currentRoundNum % self.popSize != 0): #when loop size smaller than popSize
            # Using readlines()
            with open("Inputs\\actions.txt") as fin:
                data = fin.read().splitlines(True)
                self.actions = data[(self.currentRoundNum % self.popSize)]
                self.records.append(self.actions)
                #print("inputLen",self.inputLen)
                if len(self.actions) < self.inputLen:
                    print("add")
                    self.actions = "R" + data[(self.currentRoundNum % self.popSize)]
                print("Round", self.currentRoundNum, "finished")
                print(self.actions[25:35])

        else: #for each loop finished

            #Reset records
            self.records = []

            #Read New Line
            # Using readlines()
            with open("Inputs\\actions.txt") as fin:
                data = fin.read().splitlines(True)
                self.actions = data[(self.currentRoundNum % self.popSize)]
                self.records.append(self.actions)
                if len(self.actions) < self.inputLen:
                    self.actions = "R" + data[(self.currentRoundNum % self.popSize)]
                print("Round", self.currentRoundNum, "finished")
                print(self.actions[25:35])
        # for rec in self.records:
        #     print(rec[0:5])
        #print("endGeneticAI2")
        pass
        
    ################# Processing #######################
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
            #print("Round:", self.currentRoundNum)



        if self.cc.getSkillFlag():
            self.inputKey = self.cc.getSkillKey()
            return


        self.inputKey.empty()
        self.cc.skillCancel()

        # Action List
        if len(self.actions) > 0 and self.frameData.getFramesNumber() > 1 and self.frameData.getRemainingFramesNumber() > 16:
            # print(self.actions[0])
            if(self.actions[0] == "N"): #no moves
                #print(self.frameData.getFramesNumber(), self.actions[0])
                pass
            else:
                #print(self.frameData.getFramesNumber(),self.actions[0])
                self.cc.commandCall(self.actions[0])
            self.actions = self.actions[1:]
    
######################## Close ###############################
    def close(self):
        #Store the combo data in a json file
        with open("combos.json", 'w') as file:
            json.dump(self.combos, file)
            
    
#########################################
##### The functions we leave alone ######
#########################################

    def getInformation(self, frameData, isControl):
        # Getting the frame data of the current frame
        self.frameData = frameData
        self.cc.setFrameData(self.frameData, self.player)



    # please define this method when you use FightingICE version 4.00 or later
    def getScreenData(self, sd):
        pass

    def initialize(self, gameData, player):
        # Initializng the command center, the simulator and some other things
        self.inputKey = self.gateway.jvm.struct.Key()
        self.frameData = self.gateway.jvm.struct.FrameData()
        self.cc = self.gateway.jvm.aiinterface.CommandCenter()

        self.player = player
        self.gameData = gameData
        self.simulator = self.gameData.getSimulator()
        #print("startGeneticAI")

        return 0

    def input(self):
        # Return the input for the current frame
        return self.inputKey

    # This part is mandatory
    class Java:
        implements = ["aiinterface.AIInterface"]

