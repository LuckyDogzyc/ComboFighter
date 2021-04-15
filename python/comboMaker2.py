import sys
import random
import numpy


###########################################################
# getData()
# 
# This method reads in 2 files for information:
#    actions.txt - holds action strings representing combos
#    records.txt - holds data for making the heuristic
#
# It will read each line, strip the newline character
#  and return the resulting arrrays
###########################################################
def getData():
	#Read from each file
	with open("Inputs\\actions.txt", 'r') as actions:
		combos = actions.read().splitlines(True)
	with open("Outputs\\records.txt", 'r') as records:
		comboInfo = records.read().splitlines(True)
	
	#Strip the newline character from the lines
	for i in range(len(combos)):
		combos[i] = combos[i].strip("\n")
		comboInfo[i] = comboInfo[i].strip("\n")
	
	#Return the new arrrays
	return combos, comboInfo



###########################################################
# getHeuristic(array)
#
# This method uses the array of data from records.txt to
#  generate heuristics for each action string in actions.txt
#
# It will find the longest string of '1's, then it will
#  find the nearest neighbors to the left and right and
#  measure the amount of '1's in each of them. It will
#  add to the heuristic based on the size of these groups
#  and subtract from the heuristic based on the amount
#  of space between the groups
###########################################################
def getHeuristic(records):
	heuristics = []
	for i in range(len(records)):
		biggest = 0
		biggestStart = 0
		tempStart = 0
		tempBegin = True
		biggestEnd = 0
		isBiggest = False
		count = 0
		
		#Find the biggest string of '1's
		for j in range(len(records[i])):
			if records[i][j] == '1':
				#If starting a new line of '1's
				# remember the beginning
				if tempBegin == True:
					tempBegin = False
					tempStart = j
				
				count += 1
				
				#If bigger than biggest, remember the
				# information of the biggest
				if count > biggest:
					isBiggest = True
					biggest = count
					biggestStart = tempStart
				
				
			else:
				count = 0
				tempBegin = True
				
				#If this was the biggest, remember the end
				if isBiggest == True:
					isBiggest = False
					biggestEnd = j - 1
		
		#If the last character was part of the biggest string
		# make sure biggestEnd is set
		if isBiggest == True:
			biggestEnd = len(records[i])
		
		#Get the left and right combos and space
		left = 0
		lSpace = 0
		right = 0
		rSpace = 0
		flag = False
		
		#Finds the combo to the left
		biggestStart -= 1
		while biggestStart >= 0:
			#Found the left combo, counting it
			if records[i][biggestStart] == '1':
				flag = True
				left += 1
			
			#If found the left combo, leave
			#else count the space between combos
			else:
				if flag == True:
					break
				lSpace += 1
				
			biggestStart -= 1
		
		flag = False
		#finds the combo to the right
		biggestEnd += 1
		while biggestEnd < len(records[i]):
			#Found the right combo, counting it
			if records[i][biggestEnd] == '1':
				flag = True
				right += 1
			
			#If found the right combo, leave
			#else count the space between combos
			else:
				if flag == True:
					break
				rSpace += 1
			
			biggestEnd += 1
		
		if left == 0:
			lSpace = 0
		if right == 0:
			rSpace = 0
		
		#Calculate Heuristic
		#print("biggest is ", biggest, "\nleft is ", left, "\nleft space is ",
		#		 lSpace, "\nright is ", right, "\nright space is ", rSpace)
		heuristic = int((2*biggest) + left + right - lSpace - rSpace)
		#print("heuristic for ", i , " is ", heuristic, "\n")
		heuristics.append(heuristic)
	
	#Return the array
	return heuristics
		



###########################################################
# mergeSort(arrray, array)
#
# This method sorts the arrays of action strings and 
#  heuristics using a mergeSort algorithm and sorting by
#  the heuristic value
#
# It sorts from highest heuristic to lowest
###########################################################
def mergeSort(combos, heuristics):
	#If there is only one item, return
	if len(heuristics) == 1:
		return combos, heuristics
	
	#Split the arrays in two
	mid = int(len(combos)/2)
	h1 = heuristics[:mid]
	h2 = heuristics[mid:]
	c1 = combos[:mid]
	c2 = combos[mid:]
	
	#MergeSort the two halves
	m1, h1 = mergeSort(c1, h1)
	m2, h2 = mergeSort(c2, h2)
	
	#Add the items of the arrays back into the arrays in
	# sorted order (highest heuristic to lowest)
	i = j = k = 0
	while i < len(h1) and j < len(h2):
		if h1[i] > h2[j]:
			heuristics[k] = h1[i]
			combos[k] = c1[i]
			i += 1
		else:
			heuristics[k] = h2[j]
			combos[k] = c2[j]
			j += 1
		k += 1
	
	#Add any remnants into the arrays
	while i < len(h1):
		heuristics[k] = h1[i]
		combos[k] = c1[i]
		i += 1
		k += 1
	while j < len(h2):
		heuristics[k] = h2[j]
		combos[k] = c2[j]
		j += 1
		k += 1
	
	#Return the arrays
	return combos, heuristics



###########################################################
# getProbabilities(array)
#
# This method uses the heuristics generated to calculate
#  the probabilities that each combo will be a parent of
#  the new children
###########################################################
def getProbabilities(heuristics):
	#Calculate the total amount of heuristics
	total = 0
	for i in range(len(heuristics)):
		total += heuristics[i]
	
	#Make an array for the new proabilites
	probPop = [0 for i in range(len(heuristics))]
	
	#Add the probabilites to the new array
	for i in range(len(heuristics)):
		probPop[i] = heuristics[i] / total
	
	#Return the array
	return probPop



###########################################################
# makeChildren(array, array)
#
# This method will use the combos and their probabilites
#  to generate children to populate half of the new combo
#  list
###########################################################
def makeChildren(combos, probabilities):
	#Resulting list of children
	childList = []
	
	#Loop to generate children
	for i in range(int(len(combos)/2)):
		#Select the parents
		parents = numpy.random.choice(combos, 2, p=probabilities)
		
		#Use parents to generate child
		child = []
		for i in range(len(parents[0])):
			child.append(numpy.random.choice([parents[0][i], parents[1][i]], p=[0.5,0.5]))
		
		#Mutate child
		mutateChance = 0.3
		for i in range(len(child)):
			randNum = random.random()
			if randNum <= mutateChance:
				child[i] = random.choice(['U', 'D', 'L', 'R', 'A', 'B', 'C', 'N'])
		
		#Add child to the list
		childList.append(child)
	
	#Return the array
	return childList



###########################################################
# makeNewComboList(array, array)
#
# This method creates an array containing all of the
#  children array and the first half of the combos array
###########################################################
def makeNewComboList(children, combos):
	#Make list for new combos
	newList = []
	
	#Append children to the new list
	for i in range(len(children)):
		newList.append(children[i])
	
	#Append best parents to the new list
	for i in range(int(len(combos) - len(children))):
		newList.append(combos[i])
	
	#Return the array
	return newList



###########################################################
# newActionsList(array)
#
# This method converts the arrays of characters into
#  strings and overwrites actions.txt with new combos
###########################################################
def newActionsList(combos):
	with open("Inputs\\actions.txt", 'w') as save:
		#Set to writing a print statement to the actions.txt
		# file
		sys.stdout = save
		
		#Turn the arrays of characters into strings
		finalStrings = []
		for i in range(len(combos)):
			string = ""
			for j in range(len(combos[i])):
				string += combos[i][j]
			finalStrings.append(string)
		
		#Print the new strings to actions.txt
		for i in range(len(finalStrings)):
			print(finalStrings[i])


	
###########################################################
# Main
#
# This will execute the methods for the program
###########################################################
if __name__ == '__main__':
	combos, records = getData()
	
	heuristics = getHeuristic(records)
	
	combos, heuristics = mergeSort(combos, heuristics)
	
	probPop = getProbabilities(heuristics)
	
	children = makeChildren(combos, probPop)
	
	newCombos = makeNewComboList(children, combos)
	
	newActionsList(newCombos)