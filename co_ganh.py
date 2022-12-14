from utils import *
from minimax import *


class CoGanh:
    def __init__(self):
        self.initBoard = [[0 for j in range(0, 5)] for i in range(0, 5)]
        for i in range(0, 5):
            self.initBoard[0][i] = -1
            self.initBoard[4][i] = 1
        self.initBoard[1][0] = self.initBoard[1][4] = self.initBoard[2][4] = -1
        self.initBoard[2][0] = self.initBoard[3][0] = self.initBoard[3][4] = 1
        self.board = copy(self.initBoard)
        self.preBoard = copy(self.initBoard)
        self.numOfTurn = 0

    def resetGame(self):
        self.board = copy(self.initBoard)
        self.preBoard = copy(self.preBoard)
        self.numOfTurn = 0

    def play(self, firstTurn, player1, player2):
        listBoard = [copy(self.board)]
        turn = firstTurn

        while not isWin(self.board):
            self.numOfTurn += 1
            player = player1 if turn == 1 else player2
            m = player.selectMove(self.board, self.preBoard)
            if isLegal(m):
                self.preBoard = copy(self.board)
                makeMove(self.board, m, player.playerId)
            else:
                break
            listBoard.append(copy(self.board))
            turn *= -1

        self.resetGame()
        return listBoard

    def playOne(self, player1, curBoard, preBoard):
        move = player1.selectMove(curBoard, preBoard)
        if isLegal(move):
            preBoard = copy(curBoard)
            makeMove(curBoard, move, player1.playerId)
        return isWin(curBoard), copy(preBoard), copy(curBoard)


if __name__ == '__main__':
    agent1 = MinimaxAgent(0, 1)
    agent2 = MinimaxAgent(2, -1)

    game = CoGanh()
    boards = game.play(1, agent1, agent2)

    for board in boards:
        print_board(board)
        print()
    print(f"Total steps: {len(boards)}")
