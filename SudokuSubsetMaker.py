#Developed by Olivia Bhowmik
#License: MIT

import random

#Reads the million game file and returns a list of a thousand random lines
def fileSubset():
    lineNums = []
    lines = []
    lineVals = []
    sudokuFileVals = []
    filler = []

    readFile = open("sudokuMillion.csv", "r") #reads million game file
    for i in range(1, 1000): #selects only 1000 lines
        lineRand = random.randint(1, 1000000) #randomizes the lines chosen
        if lineRand not in lineNums: #makes sure any game isn't selected twice
            lineNums.append(lineRand)
            lines.append(lineRand)
    for x, line in enumerate(readFile): #goes through the file line by line
        if x in lines:
            lineVals.append(line.strip()) #appends file data to list and strips off the "\n"
    readFile.close()

    return lineVals

#Uses the random lines from previous function to write a new gamefile with a thousand games
def subsetWriter(fileData):
    ofile_o = open('sudokuStoredGames.csv', 'w') #opens a file for writing
    ofile_o.write("quizzes, solutions\n") #writes the header
    for fileLine in fileData: #goes through each item in the previous function's data list
        ofile_o.write(fileLine) #writes each item in the file
        ofile_o.write("\n") #goes to a new line
    ofile_o.close() #closes the file

strippedData = fileSubset()
subsetWriter(strippedData)