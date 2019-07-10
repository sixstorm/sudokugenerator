from random import randint
import random
from copy import deepcopy
import copy
import time



"""

Author:  Andrew Scott

This script creates a 9x9 grid of 0s.
Going from left to right, top to bottom, each cell is tested with a random number.
If candidate passes 3 tests (box, row and column), number is set, otherwise, try the next number.
If none of the available candidates work, it will backtrack in the same row, swapping numbers to
try and make it fit.
Some times there aren't any numbers left to try, even after swapping numbers around.  In this case,
the whole row is wiped back to 0s and we start the row over again.

Verion 0.15

Currently working on:
- Generate X number of puzzles
- Gather stats:  time per puzzle, time for batch job, how many completed
- Use Pandas to generate a table?

Working:
- Export boards as 81-length string to text file



"""

global numbers
global board
global zeroAttempts
zeroAttempts = 0
numbers = 0

def main():
    global board
    start_time = time.time()
    board = generateBoard()  # Create a 9x9 grid of 0s

    # Go through each number
    for i in range(0,9):
        for j in range(0,9):
            # Evaluate number in current cell
            evaluateCell(i,j)
            print("")
    print("All done!")
    print("This Sudoku board took %s seconds to complete!" % (time.time() - start_time))
    easyBoard = makeEasy()
    printBoard(board)
    exportBoard(board,easyBoard)

def evaluateCell(row,col):
    global board
    global numbers

    # Reset test results
    rowCheck = False
    columnCheck = False
    boxCheck = False

    # If new row, generate list of numbers 1-9
    if col == 0:
        numbers = newNumbers()

    # Try each number in numbers to see if it fits in cell
    for randomNumber in numbers:
        # Take snapshot of the board
        snapshot = copy.deepcopy(board)

        print("Let's try",randomNumber)

        # Insert randomNumber into current cell and then test
        board[row][col] = randomNumber
        print("")
        print("Possible numbers:",numbers)

        if boxTest(row,col) == False or rowTest(row,col) == False or columnTest(row,col) == False:
            print("Something failed, trying the next number...")
            # Revert snapshot
            board = copy.deepcopy(snapshot)
            if randomNumber == numbers[-1]:
                swapAround(row,col,numbers)
                continue
            continue
        elif boxCheck == rowCheck == columnCheck == True:
            print("%s fits in this cell" % (randomNumber))
            numbers.remove(randomNumber)
            printBoard(board)

        # # See if number is valid in box
        # if boxTest(row,col) == False:
        #     print("Box test failed.  Reverting board!")
        #     # Revert snapshot
        #     board = copy.deepcopy(snapshot)
        #     # Re-insert randomNumber into numbers
        #     if randomNumber == numbers[-1]:
        #         swapAround(row,col,numbers)
        #         continue
        #     continue  # Continue to next number in numbers list
        # else:
        #     print("Box test check!")
        #     boxCheck = True
        #
        # # See if number is valid in row
        # if rowTest(row,col) == False:
        #     print("Row test failed.  Reverting board!")
        #     # Revert snapshot
        #     board = copy.deepcopy(snapshot)
        #     # Re-insert randomNumber into numbers
        #     if randomNumber == numbers[-1]:
        #         swapAround(row,col,numbers)
        #         continue
        #     continue
        # else:
        #     print("Row test check!")
        #     rowCheck = True
        #
        # # See if number is valid in row
        # if columnTest(row,col) == False:
        #     print("Column test failed.  Reverting board!")
        #     # Revert snapshot
        #     board = copy.deepcopy(snapshot)
        #     # Re-insert randomNumber into numbers
        #     if randomNumber == numbers[-1]:
        #         swapAround(row,col,numbers)
        #         continue
        #     continue
        # else:
        #     print("Column test check!")
        #     columnCheck = True
        #
        # # Final check
        # if boxCheck == rowCheck == columnCheck == True:
        #     print("%s fits in this cell" % (randomNumber))
        #     numbers.remove(randomNumber)
        #     printBoard(board)
        # if col == 8:
        #     print("Finished with this row...")

        break

def swapAround(row,col,numbers):
    global board

    x = 0
    while x <= col:
        rowCheck = False
        columnCheck = False
        boxCheck = False
        test1 = False
        test2 = False
        # Left to right in current row, test candidate
        print("Pass:",x)
        candidate = board[row][x]

        for number in numbers:
            # Take snapshot
            snapshot = copy.deepcopy(board)

            # Insert candidate into current row/col
            board[row][col] = number
            print("Possible numbers:",numbers)
            print("Swapping %s with %s" % (candidate,number))
            board[row][col],board[row][x] = board[row][x],board[row][col]
            print("Testing number:",number)
            print("Testing board:")
            printBoard(board)

            # Test latter cell with swapped numbers
            if boxTest(row,col) == True and rowTest(row,col) == True and columnTest(row,col) == True:
                print("Test 1 Passed!")
                test1 = True
            else:
                test1 = False
                board = copy.deepcopy(snapshot)
                print("Reverted board:")
                printBoard(board)

            # Test former cell with swapped numbers
            if boxTest(row,x) == True and rowTest(row,x) == True and columnTest(row,x) == True:
                print("Test 2 Passed!")
                test2 = True
            else:
                test2 = False
                board = copy.deepcopy(snapshot)
                print("Reverted board:")
                printBoard(board)

            # Final test
            if test1 == True and test2 == True:
                numbers.remove(number)
                break
            # If we run out of numbers to try
            elif test1 == False or test2 == False:
                if number == numbers[-1]:
                    print("Zeroing out row %s column %s ..." % (row,col))
                    zeroOutRow(row,col)
                    break
                print("One or both tests failed!")
                board = copy.deepcopy(snapshot)
                print("Reverted board:")
                printBoard(board)
            x += 1
        break

def zeroOutRow(row,col):
    global board
    global zeroAttempts

    # Go through row and zero it out
    j = 0
    while j <= col:
        print("Resetting [%s][%s]" % (row,j))
        board[row][j] = 0
        j += 1

    zeroAttempts += 1
    print("Zero attempts:",zeroAttempts)
    # If a row has been zero'd out 5 times, stop and reset
    if zeroAttempts == 20:
        print("I can't make this puzzle")
        main()

    # Redo row
    j = 0
    while j <= col:
        evaluateCell(row,j)
        j += 1

def newNumbers():
    global numbers
    print("Refilling numbers!")
    numbers = list(range(1,10))
    random.shuffle(numbers)
    print("Numbers:",numbers)
    return numbers

def boxTest(row,col):
    global board
    boxList = []

    iMin = (row // 3)
    jMin = (col // 3)
    for i in range(3*iMin,3*iMin+3):
        for j in range(3*jMin,3*jMin+3):
            boxList.append(board[i][j])

    # If number is in the box, break loop and go to next number
    if boxList.count(board[row][col]) > 1:
        return False
    else:
        return True

def rowTest(row,col):
    global board
    if board[row].count(board[row][col]) == 1:  # If only 1 instance, return true
        return True
    else:
        return False

def columnTest(row,col):
    global board
    colList = []
    for x in range(0,9):
        colList.append(board[x][col])

    if colList.count(board[row][col]) == 1:  # If only 1 instance, return true
        return True
    else:
        return False

def generateBoard():
    board = [[0 for i in range(9)] for j in range(9)]
    return board


def printBoard(board):
    for index, value in enumerate(board):
        print(*value)

def makeEasy():
    global board
    easyBoard = copy.deepcopy(board)
    easyToRemove = 20
    print("Let's make an easy puzzle")

    for _ in range(easyToRemove):
        # Get 2 random numbers between 0-8
        row = random.randint(0,8)
        column = random.randint(0,8)
        print(row,column)

        easyBoard[row][column] = 0

    print("")
    return easyBoard

def exportBoard(board,easyBoard):
    printBoard(board)
    print("")
    printBoard(easyBoard)
    export, export2 = "", ""
    exportFile = open("sudokuExport.txt","a")
    for i in range(0,9):
        for j in range(0,9):
            export += str(board[i][j])
    print(export)
    for i in range(0,9):
        for j in range(0,9):
            export2 += str(easyBoard[i][j])
    print(export2)
    exportFile.write(export + ";" + export2 + "\n")
    exportFile.close()

fake = True
while fake:
    main()
    time.sleep(3)
