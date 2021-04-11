############################################################
# This program uses a genetic algorithm to generate strings
# of actions
#
# The inputs are a list of action strings from 'Inputs\\actions.txt'
# and list of results in '1's and '0's from 'Outputs\\records.txt'
#
# The results will be used to determine the heuristic that will
# determine the probability for each action string to be the
# parent of the children being generated
#
# This program assumes that the action strings will be the same length
# for the purposes of mutating them into children of the same length
############################################################

import sys
import random
import numpy


#################### Standard MergeSort Function ###################
def merge(mergeArray, popArray):
    # only do this block if there is more than one item
    if len(mergeArray) > 1:
        # split the arrays into two parts
        mid = int(len(mergeArray) / 2)
        merge1 = mergeArray[:mid]
        pop1 = popArray[:mid]
        merge2 = mergeArray[mid:]
        pop2 = popArray[mid:]

        # MergeSort both halves
        merge1, pop1 = merge(merge1, pop1)
        merge2, pop2 = merge(merge2, pop2)

        # print('length of mergeArray is ', int(len(mergeArray)))
        # print('length of merge1 is ', int(len(merge1)))
        # print('length of merge2 is ', int(len(merge2)))

        # Sort from lowest heuristic to highest until one array runs out
        i = j = k = 0
        while i < int(len(merge1)) and j < int(len(merge2)):
            if merge1[i] < merge2[j]:
                mergeArray[k] = merge1[i]
                popArray[k] = pop1[i]
                i += 1
            else:
                mergeArray[k] = merge2[j]
                popArray[k] = pop2[j]
                j += 1
            k += 1

        # Add whatever ones were left
        while i < int(len(merge1)):
            mergeArray[k] = merge1[i]
            popArray[k] = pop1[i]
            i += 1
            k += 1
        while j < int(len(merge2)):
            mergeArray[k] = merge2[j]
            popArray[k] = pop2[j]
            j += 1
            k += 1

    # Return the sorted arrays
    return mergeArray, popArray


######################## Main ###########################
def comboMaker():
    print('Getting the files\n')
    # recieve the input and output to work with
    with open('Inputs\\actions.txt', 'r') as input:
        combos = input.read().splitlines(True)

    with open('Outputs\\records.txt', 'r') as output:
        results = output.read().splitlines(True)


    for i in range(len(combos)):
        combos[i] = combos[i].strip('\n')
        results[i] = results[i].strip('\n')

    # print(len(combos[0]))
    # print(len(combos[-1]))
    # print(len(results[0]))
    # print(len(results[-1]))
    #print(combos)

    #print('Calculating the heuristics')
    # Gather the heuristics for each combo
    heuristics = [0 for i in range(len(results))]
    for i in range(len(results)):
        for j in range(len(results[i])):
            if results[i][j] == '1':
                heuristics[i] += 1
        #print('heuristic for ', i, ' is ', heuristics[i])
    #print('\n')

    #print('Sorting the data\n')
    # Sort the actionlists by heuristic (low to high)
    heuristics, combos = merge(heuristics, combos)

    #print('Calculating the probabilities')
    # make probabilites of heuristic
    totalH = 0
    for i in range(len(heuristics)):
        totalH += heuristics[i]

    probPop = []
    for i in range(len(heuristics)):
        probPop.append(heuristics[i] / totalH)

    #print('Generating new combos')
    newComboList = []
    # Make half population size of children
    for i in range(int(len(combos) / 2)):
        #print('Building Child')
        # select parents based on percentage chance
        parents = numpy.random.choice(combos, 2, p=probPop)

        # make 50/50 chance to get action from each parent
        child = []
        for i in range(len(parents[0])):
            actionChoice = [parents[0][i], parents[1][i]]
            child.append(numpy.random.choice(actionChoice, p=[0.5, 0.5]))

        # make 70/30 chance to mutate each action
        actions = ['R', 'L', 'U', 'D', 'A', 'B', 'C', 'N']
        mutateChance = 0.7
        for i in range(len(child)):
            randChoice = random.random()
            if randChoice > mutateChance:
                child[i] = random.choice(actions)

        # add new child to the newComboList
        newComboList.append(child)

    #print('adding the best of the last combos to the new list')
    # Add the best half of the old combos to the list
    for i in range(len(combos) - len(newComboList)):
        newComboList.append(combos[i])

    print('writing new list to a text file')
    # write the new combos to a file
    with open('Inputs\\actions.txt', 'w') as saving:
        sys.stdout = saving
        finalStrings = []
        for i in range(len(newComboList)):
            finalString = ""
            for j in range(len(newComboList[i])):
                finalString += newComboList[i][j]
            finalStrings.append(finalString)

        for i in range(len(finalStrings)):
            print(finalStrings[i])

    print("DONE")