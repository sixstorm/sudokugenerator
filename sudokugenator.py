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

FUTURE PLANS
I want this "service" available as a simple website.  Someone can input their password, and the script
to create an Easy, Medium and Difficult version of the same Sudoku board, convert to a PDF that looks
good, and finally emails to said person so they can work the puzzle via touch device.

"""

global numbers
global board
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
    printBoard(board)
    print("This Sudoku board took %s seconds to complete!" % (time.time() - start_time))

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

        # If last number in row to attempt, enable lastAttempt
        if randomNumber == numbers[-1]:
            print("Last number in possibilities")
            lastAttempt = True
        else:
            lastAttempt = False

        # Take snapshot of the board
        snapshot = copy.deepcopy(board)

        print("Testing number",randomNumber)

        # Insert randomNumber into current cell and then test
        board[row][col] = randomNumber
        print("Successfully inserted",board[row][col])
        print("")
        print("Possible numbers:",numbers)

        # See if number is valid in box
        if boxTest(row,col) == False:
            print("Box test failed.  Reverting board!")
            # Revert snapshot
            board = copy.deepcopy(snapshot)
            # Re-insert randomNumber into numbers
            if lastAttempt == True:
                swapAround(row,col,numbers)
                continue
            continue  # Continue to next number in numbers list
        else:
            print("Box test check!")
            boxCheck = True

        # See if number is valid in row
        if rowTest(row,col) == False:
            print("Row test failed.  Reverting board!")
            # Revert snapshot
            board = copy.deepcopy(snapshot)
            # Re-insert randomNumber into numbers
            if lastAttempt == True:
                swapAround(row,col,numbers)
                continue
            continue
        else:
            print("Row test check!")
            rowCheck = True

        # See if number is valid in row
        if columnTest(row,col) == False:
            print("Column test failed.  Reverting board!")
            # Revert snapshot
            board = copy.deepcopy(snapshot)
            # Re-insert randomNumber into numbers
            if lastAttempt == True:
                swapAround(row,col,numbers)
                continue
            continue
        else:
            print("Column test check!")
            columnCheck = True

        # Final check
        if boxCheck == rowCheck == columnCheck == True:
            print("%s fits in this cell" % (randomNumber))
            numbers.remove(randomNumber)
            printBoard(board)
        if col == 8:
            print("Finished with this row...")

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
        lastAttempt = False
        # Left to right in current row, test candidate
        print("Pass:",x)
        candidate = board[row][x]

        for number in numbers:
            # Check for last number in numbers list
            if number == numbers[-1]:
                lastAttempt = True

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
                if lastAttempt == True:
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
    # Go through row and zero it out
    j = 0
    while j <= col:
        print("Resetting [%s][%s]" % (row,j))
        board[row][j] = 0
        j += 1

    print("Look what I did!")
    printBoard(board)

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
    print("[%s][%s]" % (row,col))
    if row // 3 == 0 and col // 3 == 0:
        activeBox = 0
    elif row // 3 == 0 and col // 3 == 1:
        activeBox = 1
    elif row // 3 == 0 and col // 3 == 2:
        activeBox = 2
    elif row // 3 == 1 and col // 3 == 0:
        activeBox = 3
    elif row // 3 == 1 and col // 3 == 1:
        activeBox = 4
    elif row // 3 == 1 and col // 3 == 2:
        activeBox = 5
    elif row // 3 == 2 and col // 3 == 0:
        activeBox = 6
    elif row // 3 == 2 and col // 3 == 1:
        activeBox = 7
    elif row // 3 == 2 and col // 3 == 2:
        activeBox = 8

    if activeBox == 0:
        for i in range(0,3):
            for j in range(0,3):
                boxList.append(board[i][j])

    if activeBox == 1:
        for i in range(0,3):
            for j in range(3,6):
                boxList.append(board[i][j])

    if activeBox == 2:
        for i in range(0,3):
            for j in range(6,9):
                boxList.append(board[i][j])

    if activeBox == 3:
        for i in range(3,6):
            for j in range(0,3):
                boxList.append(board[i][j])

    if activeBox == 4:
        for i in range(3,6):
            for j in range(3,6):
                boxList.append(board[i][j])

    if activeBox == 5:
        for i in range(3,6):
            for j in range(6,9):
                boxList.append(board[i][j])

    if activeBox == 6:
        for i in range(6,9):
            for j in range(0,3):
                boxList.append(board[i][j])

    if activeBox == 7:
        for i in range(6,9):
            for j in range(3,6):
                boxList.append(board[i][j])

    if activeBox == 8:
        for i in range(6,9):
            for j in range(6,9):
                boxList.append(board[i][j])

    # If number is in the box, break loop and go to next number
    if boxList.count(board[row][col]) > 1:
        return False
    else:
        return True

def rowTest(row,col):
    global board
    # number = board[row].count(board[row][col])
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

main()
