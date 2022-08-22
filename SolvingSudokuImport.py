#Developed by Olivia Bhowmik
#License: MIT

import os.path, sys

#Splits sudoku data into rowns and colums aka grid format
def grid(input_sudoku):
    count = 0
    RowList = []
    SudokuGrid = []

    for SuNum in input_sudoku:
        SuNum = int(SuNum)
        RowList.append(SuNum)
        count = count + 1
        if count == 9:
            SudokuGrid.append(RowList)
            RowList = []
            count = 0

    return SudokuGrid

def printGrid(unformatted_g):

    for row in unformatted_g:
        count = 0
        for i in row:
            if count < len(row) - 1:
                print(i, end=' ')
            else:
                print(i)
                #print count
            count = count + 1
        #print '\n'


def box_spec():
    AllBoxSpec = []

    ax_box = ['A', 'X', 0, 2, 0, 2]
    AllBoxSpec.append(ax_box)

    ay_box = ['A', 'Y', 0, 2, 3, 5]
    AllBoxSpec.append(ay_box)

    az_box = ['A', 'Z', 0, 2, 6, 8]
    AllBoxSpec.append(az_box)

    bx_box = ['B', 'X', 3, 5, 0, 2]
    AllBoxSpec.append(bx_box)

    by_box = ['B', 'Y', 3, 5, 3, 5]
    AllBoxSpec.append(by_box)

    bz_box = ['B', 'Z', 3, 5, 6, 8]
    AllBoxSpec.append(bz_box)

    cx_box = ['C', 'X', 6, 8, 0, 2]
    AllBoxSpec.append(cx_box)

    cy_box = ['C', 'Y', 6, 8, 3, 5]
    AllBoxSpec.append(cy_box)

    cz_box = ['C', 'Z', 6, 8, 6, 8]
    AllBoxSpec.append(cz_box)

    return AllBoxSpec

def cell_spec():
    #Small rows and colums
    CellSpec = []

    for A in range(0, 9):
        for B in range(0, 9):
            templist = []
            templist.append(A)
            templist.append(B)

            CellSpec.append(templist)

    return CellSpec

def addValsToFinalBox(baseTable, baseGrid):
    Cell_Values = []

    for li in baseTable:
            Cell_Values.append(li)

    for i in Cell_Values:
        r = i[0]
        c = i[1]
        val = baseGrid[r][c]
        i.insert(2, val)

    return Cell_Values

def addBoxesToFinalBox(baseTable, BoxSpec):

    #Row Defining
    for i in baseTable:
        rownum = i[0]
        colnum = i[1]
        for b in BoxSpec:
            r1 = b[2]
            r2 = b[3]
            c1 = b[4]
            c2 = b[5]
            if rownum in range(r1, r2 + 1) and colnum in range(c1, c2 + 1):
                i.insert(3, b[0])
                i.insert(4, b[1])

def addPosValsToFinalBox(baseTable):
    allPosVals = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    emptyPosVals = []
    empty = []

    for i in baseTable:
        if i[2] == 0:
            i.insert(5, allPosVals)
        else:
            i.insert(5, emptyPosVals)
        i.insert(6, empty)

#Indentifying the cell that needs poss value identification
def SurroundingValCheck(baseTable):
    empty = []

    for cr in range(0, 9): #counting the row
        for cc in range(0, 9): #counting the column
            for li in baseTable: #going through all cell data to identify correct cells
                if li[0] == cr and li[1] == cc: #found the right cell
                    if li[2] == 0:
                        RowValList = RowValFinder(baseTable, cr, cc)
                        ColValList = ColValFinder(baseTable, cr, cc)
                        BigRow = li[3]
                        BigCol = li[4]
                        BoxValList = BoxValFinder(baseTable, BigRow, BigCol)
                        AllPossValsList = []
                        for r in RowValList:
                            AllPossValsList.append(r)
                        for c in ColValList:
                            AllPossValsList.append(c)
                        for b in BoxValList:
                            AllPossValsList.append(b)
                        AllPossValsList = list(dict.fromkeys(AllPossValsList))
                        li[6] = AllPossValsList

#Find the existing values in a row
def RowValFinder(baseTable, row, col):
    existingRowVals = []

    for li in baseTable:
        if li[0] == row:
            if li[2] != 0:
                existingRowVals.append(li[2])

    return existingRowVals

#Find the existing values in a column
def ColValFinder(baseTable, row, col):
    existingColVals = []

    for li in baseTable:
        if li[1] == col:
            if li[2] != 0:
                existingColVals.append(li[2])

    return existingColVals

#Find the existing values in a box
def BoxValFinder(baseTable, br, bc):
    existingBoxVals = []

    for li in baseTable:
        if li[3] == br and li[4] == bc:
            if li[2] != 0:
                existingBoxVals.append(li[2])

    return existingBoxVals

#compares the poss and imposs vals
#determines what needs to be removed
#returns list of late poss vals
def LatestPossValDet(poss, imposs):
    tempPoss = []
    for possval in poss:
        if possval not in imposs:
            tempPoss.append(possval)

    return tempPoss

def DelImpossRowVals(baseTable):
    for row in baseTable:
        LatestPossVal = LatestPossValDet(row[5], row[6])
        row[5] = LatestPossVal

#if a cell has 0 for it's value and there is only 1 poss val
#the function replaces the 0 val with the poss value
def ValReplacer(baseTable):
    for row in baseTable:
        if row[2] == 0:
            l = len(row[5])
            if l == 1:
                row[2] = row[5][0] #replace the 0 val with the actual val
                row[5] = [] #empty the poss vals list
                row[6] = [] #empty the imposs vals list

carryon = True
test = False
def ExitChecker(baseTable, PassNum):
    #assume carryon is false
    AssumedCarryon = False
    if PassNum >= 10:
        return AssumedCarryon
    for row in baseTable:
        if len(row[5]) == 1:
            AssumedCarryon = True
            return AssumedCarryon

def FinalValsList(baseTable):
    FinalValsList = []
    count = 0

    for row in baseTable:
        FinalValsList.append(row[2])
        StrFinalValsList = str(FinalValsList)

    return FinalValsList

def PrintFinalGridWithBoxes(ValList):
    TempRowList = []
    FinalGridData = []
    rowcount = 0
    count = 0

    for val in ValList:
        #val = int(val)
        TempRowList.append(val)
        count = count + 1
        if count == 3 or count == 6:
            TempRowList.append("|")
        if count == 9:
            FinalGridData.append(TempRowList)
            TempRowList = []
            count = 0

    for row in FinalGridData:
        count = 0
        rowcount = rowcount + 1
        if rowcount == 4 or rowcount == 7:
            print("---------------------")
        for i in row:
            if count < len(row) - 1:
                print(i, end=' ')
            else:
                print(i)
            count = count + 1

def exportSolution(data):

    sudokuDataTable = grid(data) #fileData #SudokuData #generates sudoku data in grid format
    boxSpecTable = box_spec() #specifies box info about cells
    finalBoxTable = cell_spec() #Makes the final box
    addValsToFinalBox(finalBoxTable, sudokuDataTable)
    addBoxesToFinalBox(finalBoxTable, boxSpecTable)
    addPosValsToFinalBox(finalBoxTable)

    carryon = True
    NumberOfPasses = 0
    #for i in range(0, 1):
    while carryon == True:
        NumberOfPasses = NumberOfPasses + 1

        SurroundingValCheck(finalBoxTable)
        DelImpossRowVals(finalBoxTable)
        carryon = ExitChecker(finalBoxTable, NumberOfPasses)
        ValReplacer(finalBoxTable)

    FinalDataList = FinalValsList(finalBoxTable)
    return FinalDataList
