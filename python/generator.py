import sys
import random

def generateRandChild(): #init the random commands to control AI
	commandList = []
	for i in range(popSize): #popSize times
		actionList = ""
		for x in range(startMovetime-2):
			actionList += ("R")
		for x in range(2):
			actionList += ("N")
		for y in range(seqLen - startMovetime): #seqLen times
			actionList += (commands[random.randint(0,7)])
		commandList.append(actionList)

	# writing to file
	file2 = open("Inputs\\actions.txt", 'w')
	for line in commandList:
		file2.writelines(line + "\n")
	file2.close()


#Genetic Algorithm Customization

iterations = 0
startMovetime = 25
seqLen = 200  # maximum length of the sequences generated = frame number
popSize = 10  # size of the population to sample from
parentRand = 0.5  # chance to select action from parent 1 (50/50)
mutRand = 0.3  # chance to mutate offspring action

bestSeq = []  # best sequence to use in case iterations max out
commands = ("A","B","C","U","D","L","R","N")

commandList = []

generateRandChild()

