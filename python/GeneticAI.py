import sys
from py4j.java_gateway import get_field
import os


class GeneticAI(object):
    def __init__(self, gateway):
        self.gateway = gateway

        #init Params
        self.popSize = 10

        # init Actions
        self.actions = ""
        self.records = []

        # # Using readlines()
        with open("Inputs\\actions.txt") as fin:
            data = fin.read().splitlines(True)
            self.actions = data[0]
            self.records.append(self.actions)
            print(self.actions[:10])
        # for rec in self.records:
        #     print(rec[0:5])

        # init hit counts
        self.hitCounts = []
        self.max = 0

    def close(self):
        #Write output log for reinforcement learning agent
        #print("hit count: ", self.hitCounts)
        ## writing to file
        # original_stdout = sys.stdout  # Save a reference to the original standard output
        #
        # with open('Outputs\\hits.txt', 'w') as f:
        #     sys.stdout = f  # Change the standard output to the file we created.
        #     print(self.hitCounts)
        #     sys.stdout = original_stdout  # Reset the standard output to its original value
        pass

    def getInformation(self, frameData, isControl):
        # Getting the frame data of the current frame
        self.frameData = frameData
        self.cc.setFrameData(self.frameData, self.player)

        # please define this method when you use FightingICE version 3.20 or later
    def roundEnd(self, x, y, z):

        #print(x)
        print(-y)
        #print(z)


        if(self.currentRoundNum % self.popSize != 0): #when loop size smaller than popSize
            # Using readlines()
            with open("Inputs\\actions.txt") as fin:
                data = fin.read().splitlines(True)
                self.actions = data[(self.currentRoundNum % self.popSize)]
                self.records.append(self.actions)
                print("Round", self.currentRoundNum, "finished")
                print(self.actions[:10])

        else: #for each loop finished

            # # Generate genetic
            # os.system('python comboMaker.py')
            # print("Updated")


            # #Write new actions
            # # print("Done")
            # # for rec in self.records:
            # #     print(rec[0:5])
            # # print("reset")
            # # writing to file
            # file2 = open("Inputs\\actions.txt", 'w')
            # for line in self.records:
            #     file2.writelines(line)
            # file2.close()



            #Reset records
            self.records = []

            #Read New Line
            # Using readlines()
            with open("Inputs\\actions.txt") as fin:
                data = fin.read().splitlines(True)
                self.actions = data[(self.currentRoundNum % self.popSize)]
                self.records.append(self.actions)
                print("Round", self.currentRoundNum, "finished")
                print(self.actions[:10])
        # for rec in self.records:
        #     print(rec[0:5])

        pass

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

        return 0

    def input(self):
        # Return the input for the current frame
        return self.inputKey

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

        # get combo
        hit = self.frameData.getCharacter(self.player).getHitCount()
        # print(hit)

        # Record hits to output
        if hit > self.max:
            self.max = hit
        elif (hit < self.max) and hit == 0:
            # print(self.max)
            self.hitCounts.append(self.max)

            self.max = 0

        # Action List
        if len(self.actions) > 0:
            # print(self.actions[0])
            if(self.actions[0] == "N"): #no moves
                pass
            else:
                self.cc.commandCall(self.actions[0])
            self.actions = self.actions[1:]
        #self.cc.commandCall("A")

    # This part is mandatory
    class Java:
        implements = ["aiinterface.AIInterface"]

