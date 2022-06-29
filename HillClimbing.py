"""
@author: Muhammed Bayram

A program that solving N-Queen problem with random walls using Random Restart Hill Climbing

In Hill Climbing, first we create random board (in our case random wall in each column). Then, we create neighbour from
this board by changing position of "only" one queen in the board. After we generate all possible neighbour we evaluate
our neighbour heuristic. In this question we calculated heuristic by number of queens that attack each other. In our
problem, our goal is to reach global minima.After we evaluated each neighbour heuristic
value we compare all neighbour and select the one that has the least heuristic value. If our chosen neighbour's
heuristic is less than our parent board than our new parent is this neighbour. Otherwise,if neighbour's
heuristic is not  less than our parent board then parent board is the best solution that we can reach. If there is a
neighbour that has a least heuristic we choose this one as a parent and repeat the process until the reach goal.

However, in our question depends on wall position there may not be solution. In this case, algorithm will return the board
that has minimum threats.
"""
import numpy as np


def solveNQueen(n):
    randomRestartHillClimber(n)


def randomBoard(n, wall):
    board = []

    for i in range(n):
        randomQueenPos = np.random.randint(0, n)
        while wall[i] == randomQueenPos:
            randomQueenPos = np.random.randint(0, n)
        board.append(randomQueenPos)

    return board


def randomRestartHillClimber(n):
    currentBestSolution = []
    currentBestThreats = n

    wall = []
    for _ in range(n):
        wall.append(np.random.randint(0, n))

    # Random restart 500 times
    for _ in range(500):
        currentBoard = randomBoard(n, wall)

        while True:
            moved = False

            neighbours = generateNeighbourState(currentBoard, wall)
            for neighbour in neighbours:
                if numOfThreatenedQueens(neighbour, wall) < numOfThreatenedQueens(currentBoard, wall):
                    currentBoard = neighbour
                    moved = True

            # If the current board has 0 threats than we find our optimal solution
            if numOfThreatenedQueens(currentBoard, wall) == 0:
                break

            # If we have checked all our neighbours and not moved then our board
            # is the best for this loop, and we can leave
            if moved != True:
                break

        if numOfThreatenedQueens(currentBoard, wall) < currentBestThreats:
            currentBestThreats = numOfThreatenedQueens(currentBoard, wall)
            currentBestSolution = list(currentBoard)
            if currentBestThreats == 0:
                break

    print("Random Restart Hill Climber\nBest solution found:", currentBestSolution,
          "with", currentBestThreats, "threats")
    drawTheBoard(wall, currentBestSolution, n)


def drawTheBoard(wall, queen, n):
    board = [['.' for x in range(n)] for y in range(n)]

    for i in range(n):
        board[wall[i]][i] = 'W'
        board[queen[i]][i] = 'Q'

    for i in range(len(board)):
        print(' '.join(board[i]))


def generateNeighbourState(board, wall):
    neighbours = []
    for c, r in enumerate(board):

        neighbour = list(board)

        for x in range(0, len(board)):
            if x != r and x != wall[c]:
                neighbour[c] = x
                neighbours.append(neighbour)
                neighbour = list(board)
    return neighbours


# Heuristic Function
def numOfThreatenedQueens(board, currentWall):

    threatenedQueens = 0
    for column, row in enumerate(board):
        threatenedQueens += isQueenThreatened(board, currentWall, column, row)

    return threatenedQueens


def isQueenThreatened(board, currentWall, queenColumn, queenRow):
    totalThreats = 0

    for column, row in enumerate(board):
        queenOnRow = 0
        queenOnLeftDiag = 0
        queenOnRightDiag = 0

        # Check row for queens
        if row == queenRow and queenColumn < column:

            if abs(queenColumn - column) <= 1:
                queenOnRow = queenOnRow + 1

            else:
                for i in range(queenColumn + 1, column):
                    if currentWall[i] != queenRow:
                        queenOnRow = queenOnRow + 1
                    else:
                        queenOnRow = 0

        # If more then 1 queen in row then there is a threat
        if queenOnRow > 0:
            totalThreats += 1

        # Check left diagonal for queens
        if (column - queenColumn) == (row - queenRow) and queenColumn < column:
            if abs(queenColumn - column) <= 1:
                queenOnLeftDiag = queenOnLeftDiag + 1
            else:
                for i in range(queenColumn + 1, column):
                    if currentWall[i] - i != queenColumn - queenRow:
                        queenOnLeftDiag = queenOnLeftDiag + 1
                    else:
                        queenOnLeftDiag = 0

        # If more then 1 queen on left diagonal then there is a threat
        if queenOnLeftDiag > 0:
            totalThreats += 1

        # Check right diagonal for queens
        if (queenColumn - column) == -(queenRow - row) and queenColumn < column:
            if abs(queenColumn - column) <= 1:
                queenOnRightDiag = queenOnRightDiag + 1
            else:
                for i in range(queenColumn + 1, column):
                    if currentWall[i] + i != queenRow + queenColumn:
                        queenOnRightDiag = queenOnRightDiag + 1
                    else:
                        queenOnRightDiag = 0

        # If more then 1 qeen on right diagonal then there is a threat
        if queenOnRightDiag > 0:
            totalThreats += 1

    return totalThreats


if __name__ == '__main__':
    n = 5
    solveNQueen(n)
