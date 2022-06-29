"""
@author: Muhammed Bayram

A program that solving N-Queen problem with random walls using Depth First Search

In DFS, we go step by step, first place the first queen than second, third, fourth. If we cannot find a place for
current queen we turn back to previous board configuration and try to other place for previous queen and run same logic
until find a solutions. Also,there can be no solution.In this case, we try all possible board configuration
and there is no solution for any board configuration.

W = wall,  Q = queen   . = empty/free place

Note: When n=3 there can be no solution, for instance:
             W   W   W
             .   .   .   for this board configuration there is no solution such that no queen attack each other
             .   .   .

But if you re-run the program multiple times eventually it will find a solution.
             Q   W   W
             W   .   Q    like that
             Q   .   .

For other n values (4 etc.) there can be no solution too. Everything depend on board configuration.
"""

import numpy as np


# create nxn board with random wall in each column
class Board:
    def __init__(self, n):
        self.n = n
        self.board = [[' . ' for x in range(n)] for y in range(n)]

        for j in range(n):
            randomWallRow = np.random.randint(0, n)
            self.board[randomWallRow][j] = ' W '

    # check is current row-col position is proper for putting queen
    def isValidMove(self, row, col):
        if self.board[row][col] != ' W ' and self.board[row][col] != ' Q ':
            if self.validity(row, col):
                return True
        return False

    def validity(self, row, col):
        top_left_diag = col
        bottom_left_diag = col
        bottom_right_diag = col
        top_right_diag_ = col

        colFlag = True
        rowFlag = True
        leftDiagFlag = True
        rightDiagFlag = True

        for i in range(n):

            # row check
            if self.board[row][i] == ' Q ':
                if abs(i - col) == 1:  # if there is no extra place between quinn return false
                    return False
                elif abs(i - col) > 1:
                    if i > col:
                        for j in range(col + 1, i):
                            if self.board[row][j] == ' W ':
                                rowFlag = True
                            else:
                                rowFlag = False
                    elif i < col:
                        for j in range(i + 1, col):
                            if self.board[row][j] == ' W ':
                                rowFlag = True
                            else:
                                rowFlag = False
                    if (rowFlag == False):
                        return False

            # col check
            if self.board[i][col] == ' Q ':
                if abs(i - row) == 1:
                    return False
                elif abs(i - row) > 1:
                    if i > row:
                        for j in range(row + 1, i):
                            if self.board[j][col] == ' W ':
                                colFlag = True
                            else:
                                colFlag = False
                    elif i < row:
                        for j in range(i + 1, row):
                            if self.board[j][col] == ' W ':
                                colFlag = True
                            else:
                                colFlag = False
                    if (colFlag == False):
                        return False

        # threat check for top left diagonal and bottom right diagonal
        for i in range(row, -1, -1):
            if top_left_diag >= 0 and self.board[i][top_left_diag] == ' Q ':
                if abs(i - row) == 1:
                    return False
                elif abs(i - row) > 1:
                    for j in range(i, row):
                        if self.board[j][j + col - row] == ' W ':
                            leftDiagFlag = True
                    else:
                        leftDiagFlag = False
                if leftDiagFlag == False:
                    return False

            if bottom_right_diag < self.n and self.board[i][bottom_right_diag] == ' Q ':
                if abs(i - row) == 1:
                    return False
                elif abs(i - row) > 1:
                    for j in range(i, row):
                        if self.board[j][row + col - j] == ' W ':
                            rightDiagFlag = True
                    else:
                        rightDiagFlag = False
                if rightDiagFlag == False:
                    return False
            top_left_diag -= 1
            bottom_right_diag += 1

        #  threat check for top right diagonal and bottom left diagonal
        for i in range(row, n):
            if bottom_left_diag < self.n and self.board[i][bottom_left_diag] == ' Q ':
                if abs(i - row) == 1:
                    return False
                elif abs(i - row) > 1:
                    for j in range(i, row):
                        if self.board[j][j + col - row] == ' W ':
                            leftDiagFlag = True
                    else:
                        leftDiagFlag = False
                if leftDiagFlag == False:
                    return False

            if top_right_diag_ >= 0 and self.board[i][top_right_diag_] == ' Q ':
                if abs(i - row) == 1:
                    return False
                elif abs(i - row) > 1:
                    for j in range(i, row):
                        if self.board[j][row + col - j] == ' W ':
                            rightDiagFlag = True
                    else:
                        rightDiagFlag = False
                if rightDiagFlag == False:
                    return False

            bottom_left_diag += 1
            top_right_diag_ -= 1

        return leftDiagFlag and rightDiagFlag and rowFlag and colFlag
        # return True

    def placeQueen(self, row, col, placedQueens):
        self.board[row][col] = ' Q '
        placedQueens += 1
        return placedQueens

    def removeQueen(self, row, col, placedQueens):
        self.board[row][col] = ' . '
        placedQueens -= 1
        return placedQueens

    def outputFormat(self):
        return [''.join(x) for x in self.board]

    def drawCompleteBoard(self, output):
        if len(output) == 0:
            print("There is no solution for this board configuration")
            self.drawEmptyBoard(self.board)

        else:
            for i in range(len(output)):
                for j in range(len(output[i])):
                    print(output[i][j])
                print("")

    def drawEmptyBoard(self, wall):
        for i in range(len(wall)):
            print(' '.join(wall[i]))


def solveNQueens(n):
    output = []
    board = Board(n)
    placedQueens = 0

    def dfs(board, n, placedQueens):
        if placedQueens == n:  # that means we put all queens to the board
            if (len(output) < 1):
                output.append(board.outputFormat())
            return

        if (len(output) < 1):
            for row in range(n):
                for col in range(n):
                    isValid = board.isValidMove(row, col)
                    if isValid:
                        placedQueens = board.placeQueen(row, col, placedQueens)
                        dfs(board, n, placedQueens)  # recursive call
                        placedQueens = board.removeQueen(row, col, placedQueens)  # turn back to previous board

    dfs(board, n, placedQueens)
    board.drawCompleteBoard(output)


if __name__ == '__main__':
    n = 5
    solveNQueens(n)
