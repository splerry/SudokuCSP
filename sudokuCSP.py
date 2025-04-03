import csv
import copy
import sys
import time
from datetime import timedelta

#Marcel Bieganski, created in CS480 (Artificial Intelligence & Machine Learning) @ Illinois Institute of Technology

class csp:

    class cspNode:
        #create board state at leaf: vars:= dictionary of (x coord, y coord): int val 1-9, constraint:= dictionary of (x coord, y coord): list[0...9] containing values x, y CANNOT be, parent:= previous board state in subtree, 
        def __init__(self, vars, constraint, parent = None):
            self.vars = vars
            self.parent = parent
            self.constraint = constraint
        def __str__(self):
            pass

        def __repr__(self):
            return str(self)
    #initializes game: mode:= method of solving puzzle 1-3, testcase:= initial board state at start loaded from .csv file, domain:= dictionary of (x coord, y coord): list[0...9] containing values x, y CAN be, inputPuzzle:= dictionary representation of initial board state, count:= used to track # of expanded nodes
    def __init__(self):
        self.mode = 0
        self.testcase = ""
        self.domain = {}
        self.inputPuzzle = {}
        self.count = 0

    
    #solves game by continuously generating board states until one is correct
    def bruteForce(self, initialState, setConstraint):
        startNode = self.cspNode(parent=None, vars=initialState, constraint=setConstraint)
        queue = []
        queue.append((0, startNode))
        while queue:
            current = queue.pop()[1]
            editVal = None
            found = False
            #finds first spot on board with no value -> ie. '0'. Starts at 0, 0 -> 8, 8
            for i in range(0, 9):
                for j in range(0, 9):
                    if current.vars[(i, j)] == 0:
                        editVal = (i, j)
                        found = True
                        break
                if found:
                    break
            #returns board state as is if it is complete -> ie. no '0' slots left
            if editVal == None or found == False:
                return (current, self.count)
            
            found = False

            #if empty slot found, cycle through all values in x, y's domain, if that value violates no constraints, a new board state is added to the queue with that value i in that slot
            for i in self.domain[editVal]:
                stop = False
                if i not in current.constraint[editVal] and self.smallGridCheck(current, editVal, i):
                    if stop == False:
                        tempVars = copy.deepcopy(current.vars)
                        tempVars[editVal] = i

                        tempConstraint = copy.deepcopy(current.constraint)
                        for j in range(0, 9):
                            if i not in tempConstraint[(editVal[0], j)] and (editVal[0], j) != editVal:
                                tempConstraint[(editVal[0], j)].append(i)
                            if i not in tempConstraint[(j, editVal[1])] and (j, editVal[1]) != editVal:
                                tempConstraint[(j, editVal[1])].append(i)
                        self.count = self.count + 1
                        tempCount = 0
                        for key, value in current.vars.items():
                            if value == 0:
                                tempCount = tempCount + 1

                        queue.append((tempCount, self.cspNode(vars=tempVars, parent=current, constraint=tempConstraint)))
                        queue.sort(key=lambda x: x[0], reverse=True)

    #given board state, checks that 1) all rows have no duplicate values, 2) all columns have no duplicate values, 3) all 3x3 subgrids have no duplicate values
    def checkCorrect(self, cspNode):
        for key, value in cspNode.vars.items():
            if value == 0:
                return "0 value detected"
            
            for i in range(0, 9):
                if cspNode.vars[(key[0], i)] == value and (key[0], i) != key:
                    return "Column error detected at (" + str(key[0]) + ", " + str(i)
                if cspNode.vars[(i, key[1])] == value and (i, key[1]) != key:
                    return "row error detected at (" + str(i) + ", " + str(key[0])
            
            place = True

            startRow = key[0] - (key[0] % 3)
            startCol = key[1]-(key[1] % 3)

            row = [0, 1, 2]
            col = [0, 1, 2]

            for i in row:
                for j in col:
                    if cspNode.vars[(startRow + i, startCol + j)] == value and (startRow + i, startCol + j) != key:
                        return "Little grid error detected at (" + str(startRow + i) + ", " + str(startCol + j) + ")"
            
        return True
                

    #initiates the recursive backtrack CSP search with MRV heuristics disabled
    def backtrackSearch(self, initialState, constraint):
        startNode = self.cspNode(parent=None, vars=initialState, constraint=constraint)
        count = 0
        return self.recursiveBacktrack(startNode, mrv=False)
    
    #initiates the recursive backtrack CSP search with MRV heuristics enabled
    def mrvBacktrackSearch(self, initialState, constraint):
        startNode = self.cspNode(parent=None, vars=initialState, constraint=constraint)
        count = 0
        return self.recursiveBacktrack(startNode, mrv=True)
    
    #given board state, creates list of all unfilled '0' slots, and orders them by possible values, list[0] having the fewest -> list[len(list)] having the most
    def sortMRV(self, cspNode):
        board = copy.deepcopy(cspNode.vars)
        tempList = []

        for vars in board.keys():
            if board[vars] == 0:
                mrv = len(self.domain[vars]) - len(cspNode.constraint[vars])
                tempList.append((vars, mrv))
        
        if len(tempList) == 0:
            return tempList
        else:
            return sorted(tempList, key=lambda x: x[1])

    #solves the game by recursively generating board state nodes, and if one violates a constraint, it resumes the search at the parent of failed node and trys other value options
    def recursiveBacktrack(self, cspNode, mrv):
        editVal = None
        found = False
        self.count = self.count + 1

        #uses self.sortMRV to find available node with least possible values
        if mrv == False:
            for i in range(0, 9):
                for j in range(0, 9):
                    if cspNode.vars[(i, j)] == 0:
                        editVal = (i, j)
                        found = True
                        break
                if found:
                    break
        else:
            sortedMRV = self.sortMRV(cspNode)
            if len(sortedMRV) > 0:
                editVal = sortedMRV[0][0]
                found = True

        #returns current board state if it is a solution
        if editVal == None or found == False:
            return (cspNode, self.count)
        
        #loops through the domain of current x, y coord pair, if the value does not violate any constraints, it expands that board states subtree. Else, it cancels that subtree and reverts current node back to that subtree's parent
        for i in self.domain[editVal]:
                stop = False
                if i not in cspNode.constraint[editVal] and self.smallGridCheck(cspNode, editVal, i):
                    '''print("FOUND VALUE " + str(i))'''
                    if mrv == True:
                        for k in range(0, 9):
                            if (editVal[0], k) != editVal and len(self.domain[(editVal[0], k)]) == 1 and i in self.domain[(editVal[0], k)]:
                                stop = True
                            if (k, editVal[1]) != editVal and len(self.domain[(k, editVal[1])]) == 1 and i in self.domain[(k, editVal[1])]:
                                stop = True
                            
                    if stop == False:

                        tempVars = copy.deepcopy(cspNode.vars)
                        tempVars[editVal] = i

                        tempConstraint = copy.deepcopy(cspNode.constraint)
                        for j in range(0, 9):
                            if i not in tempConstraint[(editVal[0], j)] and (editVal[0], j) != editVal:
                                tempConstraint[(editVal[0], j)].append(i)
                            if i not in tempConstraint[(j, editVal[1])] and (j, editVal[1]) != editVal:
                                tempConstraint[(j, editVal[1])].append(i)

                        result = self.recursiveBacktrack(self.cspNode(vars=tempVars, parent=cspNode, constraint=tempConstraint), mrv)
                        if result != None:
                            return result
        return None

    #checks to see if entry (num) is valid for that entry's x, y pairing's 3x3 subgrid
    def smallGridCheck(self, cspNode, coord, num):
        place = True

        startRow = coord[0] - (coord[0] % 3)
        startCol = coord[1]-(coord[1] % 3)

        row = [0, 1, 2]
        col = [0, 1, 2]

        for i in row:
            for j in col:
                if cspNode.vars[(startRow + i, startCol + j)] == num:
                    place = False

        return place 

    #prints out all results
    def sudokuPrint(self, cspNode, totTime, count):

        if cspNode == None:
            print("SOLUTION NOT FOUND!")
        else:

            print("Input Puzzle: ")
            printString = ""
            for i in range(0, 9):
                for j in range(0, 9):
                    printString = printString + str(self.inputPuzzle[(i, j)]) + ", "
                print(printString)
                printString = ""
            print(" ")
            
            print("Number of search tree nodes generated: " + str(count))
            print("Search time: " + str(totTime) + " seconds")

            print(" ")
            print("Solved Puzzle: ")
            printString = ""
            for i in range(0, 9):
                for j in range(0, 9):
                    if cspNode.vars[(i, j)] == 0:
                        printString = printString + "X" + ", "
                    else:
                        printString = printString + str(cspNode.vars[(i, j)]) + ", "
                print(printString)
                printString = ""
            print(" ")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        try:
            mode = sys.argv[1]
            testcase = sys.argv[2]
            testCSP = csp()

            boardStart = []

            with open(testcase, 'r') as boardcsv:
                boardreader = csv.reader(boardcsv)
                for row in boardreader:
                    boardStart.append(row)
        except FileNotFoundError:
            print("ERROR: Not enough/too many/illegal input arguments.")
            exit()

        initialState = {}
        constraint = {}

        for i in range(0, len(boardStart)):
            for j in range(0, len(boardStart[i])):
                constraint[(i, j)] = []
                initialState[(i, j)] = 0
                if boardStart[i][j] == 'X':
                    testCSP.domain[(i, j)] = list(range(1, 10))
                    testCSP.inputPuzzle[(i, j)] = 'X'
                else:
                    testCSP.domain[(i, j)] = [int(boardStart[i][j])]
                    testCSP.inputPuzzle[(i, j)] = int(boardStart[i][j])

        print("Input file: " + testcase)

        if mode == '1':
            print("Algorithm: Bruteforce search")
            print("")
            start_time = time.monotonic()
            solution = testCSP.bruteForce(initialState, constraint)
            testCSP.sudokuPrint(solution[0], time.monotonic() - start_time, solution[1])
            if testCSP.checkCorrect(solution[0]):
                print("This is a valid, solved, Sudoku puzzle")
            else:
                print("ERROR: This is not a solved Sudoku puzzle")

        elif mode == '2':
            print("Algorithm: Recursive CSP backtrack search")
            print("")
            start_time = time.monotonic()
            solution2 = testCSP.backtrackSearch(initialState, constraint)
            testCSP.sudokuPrint(solution2[0], time.monotonic() - start_time, solution2[1])
            if testCSP.checkCorrect(solution2[0]):
                print("This is a valid, solved, Sudoku puzzle")
            else:
                print("ERROR: This is not a solved Sudoku puzzle")
        elif mode == '3':
            print("Algorithm: Recursive CSP backtrack search with MRV heuristics and forward checking")
            print("")
            start_time = time.monotonic()
            solution3 = testCSP.mrvBacktrackSearch(initialState, constraint)
            testCSP.sudokuPrint(solution3[0],time.monotonic() - start_time, solution3[1])
            if testCSP.checkCorrect(solution3[0]):
                print("This is a valid, solved, Sudoku puzzle")
            else:
                print("ERROR: This is not a solved Sudoku puzzle")
    else:
        print("ERROR: Not enough/too many/illegal input arguments.")