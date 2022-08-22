#Developed by Olivia Bhowmik
#License: MIT

import os.path, sys, random, csv
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import SolvingSudokuImport

#gameFile = "sudokuMillion.csv"
gameFile = "sudokuStoredGames.csv"
#linesToChooseFrom = 1000000
linesToChooseFrom = 1000
numGames = 1000
#-------------------------------------------------------------------------------

root = Tk()
root.geometry("500x400")
root.title("Sudoku Solver Game")

frm = ttk.Frame(root, padding=20)
frm.grid()

#-----------------------------Functions-----------------------------------------
def readSudokuData(inputData):
    row = []
    inputTable = []
    count = 0
    for i in inputData:
        row.append(int(i))
        count = count + 1
        if count == 9:
            inputTable.append(row)
            row = []
            count = 0

    return inputTable

def displaySudokuTable(sudokuData):
    columnCount = 0
    rowCount = 0

    for row in sudokuData:
        for digit in row:
            labelStyle = "flat"
            if columnCount == 11:
                columnCount = 0
            if columnCount == 3 or columnCount == 7:
                ttk.Label(frm, text=" "*5, relief=labelStyle, font=20).grid(column=columnCount, row=rowCount)
                columnCount = columnCount + 1
            if digit == 0:
                digit = "_"
                ttk.Label(frm, text=digit, relief=labelStyle, font=20, foreground="red").grid(column=columnCount, row=rowCount, padx=(0,10))
                columnCount = columnCount + 1
            else:
                ttk.Label(frm, text=digit, relief=labelStyle, font=20).grid(column=columnCount, row=rowCount, padx=(0,10))
                columnCount = columnCount + 1
        rowCount = rowCount + 1
        if rowCount == 3 or rowCount == 7:
            ttk.Label(frm, text="  ", relief=labelStyle, font=20).grid(column=columnCount, row=rowCount)
            rowCount = rowCount + 1


def displaySudokuTableSolved(sudokuData, sudokuSolu):
    columnCount = 0
    rowCount = 0
    labelStyle = "flat"

    for (data, solution) in zip(sudokuData, sudokuSolu):
        if rowCount == 11:
            rowCount = 0
        if columnCount == 11:
            columnCount = 0
            rowCount = rowCount + 1
        if columnCount == 3 or columnCount == 7:
            ttk.Label(frm, text=" "*5, relief=labelStyle, font=20).grid(column=columnCount, row=rowCount)
            columnCount = columnCount + 1
        if rowCount == 3 or rowCount == 7:
            ttk.Label(frm, text="  ", relief=labelStyle, font=20).grid(column=columnCount, row=rowCount)
            rowCount = rowCount + 1
        if data == "0":
            ttk.Label(frm, text=solution, relief=labelStyle, font=20, foreground="green").grid(column=columnCount, row=rowCount, padx=(0,10))
            columnCount = columnCount + 1
            #rowCount = rowCount + 1
        else:
            ttk.Label(frm, text=solution, relief=labelStyle, font=20).grid(column=columnCount, row=rowCount, padx=(0,10))
            columnCount = columnCount + 1
            #rowCount = rowCount + 1

def compareData(value, solution):
    return [i for i in range(len(value)) if value[i] != solution[i]]

"""
def fileReader():
    games = []
    with open(gameFile, 'r') as file:
        sudokuReader = csv.reader(file)
        for x, line in enumerate(file):
            line.strip()
            games.append(line)

    return games
"""
def fileReader():
    global linesToChooseFrom, numGames
    lineNums = []
    lineVals = []
    filler = []
    sudokuFileVals = []
    with open(gameFile, 'r') as file:
        sudokuReader = csv.reader(file)
        for i in range(0, numGames):
            lineRand = random.randint(1, linesToChooseFrom)
            lineNums.append(lineRand)
        for x, line in enumerate(file):
            if x in lineNums:
                lineVals.append(line.strip())

        for fullVal in lineVals:
            for d in fullVal:
                if d == ",":
                    sudokuFileVals.append("".join(filler))
                    filler = []
                    break
                else:
                    filler.append(str(d))

    return sudokuFileVals

def finalDataToString(finalInt):
    finalStr = ""
    for num in finalInt:
        finalStr += str(num)

    return finalStr

def cancelChecker():
    msg = messagebox.askyesno("Cancel", "Do you want to cancel?")
    if msg == True:
        root.destroy()
    else:
        pass

def solutionMode():
    global dataSelect, newGame, gameMode, solution
    dataSelect = SudokuSolution
    #data = readSudokuData(dataSelect)
    #displaySudokuTable(data)
    displaySudokuTableSolved(SudokuData, dataSelect)

    solution.config(state="disabled")
    gameModeButton.config(state="normal")

def gameMode():
    global dataSelect, newGame, solution, gameMode
    dataSelect = SudokuData
    data = readSudokuData(dataSelect)
    displaySudokuTable(data)

    gameModeButton.config(state="disabled")
    solution.config(state="normal")

def newGame():
    global dataSelect, line, SudokuData, SudokuSolution, gameMode, solution, newGame
    SudokuData = random.choice(line)
    SudokuSolution = finalDataToString(SolvingSudokuImport.exportSolution(SudokuData))
    dataSelect = SudokuData
    data = readSudokuData(dataSelect)
    displaySudokuTable(data)

    gameModeButton.config(state="disabled")
    solution.config(state="normal")

def aboutBttn():
    abtMsg = messagebox.showinfo("About", "SudokuSolver is a program that offers a random sudoku game to the user from a database of a thousand stored games. The games are stored in a simple format and can be added to in the game file. The program solves the game itself using it's internal solver logic and displays the result on request.\n\nDeveloped by Olivia Bhowmik\nEmail: developer.olivia.bhowmik@gmail.com\nGame File: sudokuStoredGames.csv\nLicense: MIT\nVersion: 1.0.0\nTechnology: Tkinter GUI and Python 3")

def helpBttn():
    helpMsg = messagebox.showinfo("Help", "Welcome to SudokuSolver!\n\nFill in the missing numbers in the red underlines\nTo show the right answers click the 'Show Solution' button\nTo go back to game mode click 'Show Game Mode'\nTo exit the program click 'Cancel'")

line = fileReader()
SudokuData = random.choice(line)
SudokuSolution = finalDataToString(SolvingSudokuImport.exportSolution(SudokuData))

dataSelect = SudokuData

cancel = ttk.Button(frm, text="Cancel", command=cancelChecker, width=17).grid(column=14, row=0)
cancelSpacer = ttk.Label(frm, text=" "*15).grid(column=13, row=0)
cancelSpacer2 = ttk.Label(frm, text=" "*15).grid(column=14, row=1)

solution = ttk.Button(frm, text="Show Solution", command=solutionMode, width=17)
solution.grid(column=14, row=4)
solutionSpacer = ttk.Label(frm, text=" "*15).grid(column=13, row=4)
solutionSpacer2 = ttk.Label(frm, text=" "*15).grid(column=14, row=5)

gameModeButton = ttk.Button(frm, text="Show Game Mode", command=gameMode, width=17)
gameModeButton.grid(column=14, row=2)
gameSpacer = ttk.Label(frm, text=" "*15).grid(column=13, row=2)
gameSpacer2 = ttk.Label(frm, text=" "*15).grid(column=14, row=3)

newGame = ttk.Button(frm, text="New Game", command=newGame, width=17)
newGame.grid(column=14, row=6)
newSpacer = ttk.Label(frm, text=" "*15).grid(column=13, row=6)
newSpacer2 = ttk.Label(frm, text=" "*15).grid(column=14, row=7)

aboutButton = ttk.Button(frm, text="About", command=aboutBttn, width=17)
aboutButton.grid(column=14, row=8)
aboutSpacer = ttk.Label(frm, text=" "*15).grid(column=13, row=8)
aboutSpacer2 = ttk.Label(frm, text=" "*15).grid(column=14, row=9)

helpButton = ttk.Button(frm, text="Help", command=helpBttn, width=17)
helpButton.grid(column=14, row=10)
helpSpacer = ttk.Label(frm, text=" "*15).grid(column=13, row=10)
helpSpacer2 = ttk.Label(frm, text=" "*15).grid(column=14, row=11)

gameMode()

root.mainloop()