# sudokugenerator
Sudoku Generator

About:  This little project took me a month and 10 different attempts to figure a working algorthm out on my own (very novice Python guy here).

This script creates a complete Sudoku board from scratch.  It starts by creating a 9x9 grid of 0s (2D list), then going through each number (left to right, top to bottom) and testing each cell with random numbers (technically brute force).  

If it gets to a test failure, it will try the next possible unused number.  If there are no more possible numbers to try, it will try to swap with numbers already set in the row to see if there is a better fit, starting with the first number in the row.  Finally, if all else fails, the entire row gets reset to 0s and the process of finding the right number starts over again until something works.

My code is horrible, I know, but it works.  I plan on cleaning up my code, making it more "Python-y" and of course, I have bigger future plans for this little guy. 

Hope that someone can learn from this way of generating a Sudoku board.
