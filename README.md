# SudokuCSP
Demonstrates knowledge of Constraint Satisfaction Problem solving using Sudoku. Code uses three different methods of increasing efficiency: bruteforce, CSP backtracking, and CSP backtracking with Minimum Remaining Values (MRV) heuristics and forward checking
-----------------------------------------------------------------------------------------------------------------------------------------------------------
Usage: 
have sudokuCSP.py in the same folder of at least one testcase file (1, 2, or 6 contained in repo)
Via command line (Windows) navigate to containing folder and run via command: $py ./sudokuCSP.py X testcaseY.csv
  where 'X' is the algorithm chosen (1, 2, 3) and 'Y' is the number of the ran testcase (1, 2, 6)
  Algorithm modes: 1 - bruteforce 2 - CSP backtracking (no forward checking or heuristic) 3 - CSP backtracking with forward checking and MRV heuristics (minimum remaining values)
  test case modes: 1 - hard/nearly empty board (takes longest time) 2 - medium difficulty board 3 - easy board (takes shortest time)
Expected output:
![/assets/images/githubsudokurepo1.png]
------------------------------------------------------------------------------------------------------------------------------------------------------------

This repo comes with three starting boards included, though these boards can be edited in any text editor and changed to user preference to fit any sudoku puzzle

HARD PUZZLE:
6, X, X, X, 4, X, X, 2, X,
X, X, X, X, X, X, X, X, X,
X, X, X, X, 9, X, X, X, X,
X, X, X, X, X, 2, X, 6, X,
X, X, X, X, X, 4, 7, X, X,
X, X, X, 6, X, X, X, X, X,
1, X, 2, X, X, X, X, X, X,
X, X, X, 7, X, X, X, X, X,
X, X, X, 5, X, 6, X, X, 4,

MEDIUM PUZZLE:
X, 6, X, 2, X, 4, X, 5, X,
4, 7, X, X, 6, X, X, 8, 3,
X, X, 5, X, 7, X, 1, X, X,
9, X, X, 1, X, 3, X, X, 2,
X, 1, 2, X, X, X, 3, 4, X,
6, X, X, 7, X, 9, X, X, 8,
X, X, 6, X, 8, X, 7, X, X,
1, 4, X, X, 9, X, X, 2, 5,
X, 8, X, 3, X, 5, X, 9, X,

EASY PUZZLE:
8, 6, 1, 2, 3, 4, 9, 5, 7,
4, 7, 9, 5, 6, 1, 2, 8, 3,
3, 2, 5, 9, 7, 8, 1, 6, 4,
9, 5, 8, 1, 4, 3, 6, 7, 2,
7, 1, 2, 8, 5, 6, 3, 4, 9,
6, 3, 4, 7, 2, 9, 5, 1, 8,
5, 9, 6, 4, 8, 2, 7, 3, 1,
1, X, 3, X, 9, X, 8, 2, 5,
X, 8, X, 3, X, 5, 4, 9, 6,

