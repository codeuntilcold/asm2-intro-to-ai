from utils import *
import random


class MinimaxAgent:
    def __init__(self, level, playerId):
        self.depth = level
        self.playerId = playerId

    def minSearch(self, curBoard, preBoard, depth, alpha, beta):
        moves = getValidMoves(curBoard, preBoard, -self.playerId)
        if depth == 0 or len(moves) == 0:
            return self.evaluate(curBoard)

        value = 100
        for m in moves:
            clone = copy(curBoard)
            makeMove(clone, m, -self.playerId)
            value = min(value, self.maxSearch(
                clone, curBoard, depth - 1, alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)
        # print("min", depth, value)

        return value

    def maxSearch(self, curBoard, preBoard, depth, alpha, beta):
        moves = getValidMoves(curBoard, preBoard, self.playerId)
        if depth == 0 or len(moves) == 0:
            return self.evaluate(curBoard)

        value = -100
        for m in moves:
            clone = copy(curBoard)
            makeMove(clone, m, self.playerId)
            value = max(value, self.minSearch(
                clone, curBoard, depth - 1, alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        # print("max", depth, value)

        return value

    def selectMove(self, curBoard, preBoard):
        moves = getValidMoves(curBoard, preBoard, self.playerId)
        if isNewGame(curBoard, preBoard) or self.depth == 0:
            return random.choice(moves)

        bestMoves = []
        bestValues = []
        bestSoFar = -100
        beta = 100

        if len(moves) == 0:
            return Move(Position(-1, -1), Position(-1, -1))
        if len(moves) == 1:
            return moves[0]

        for m in moves:
            nextBoard = copy(curBoard)
            makeMove(nextBoard, m, self.playerId)
            value = self.minSearch(nextBoard, curBoard,
                                   self.depth - 1, bestSoFar, beta)
            if value >= bestSoFar:
                bestSoFar = value
                bestMoves.append(m)
                bestValues.append(value)

        bestMove = random.choice([move for (move, value) in zip(
            bestMoves, bestValues) if value >= bestSoFar])

        return bestMove

    def evaluate(self, board):
        score = 0
        for i in range(0, 5):
            for j in range(0, 5):
                if board[i][j] == self.playerId:
                    score += 1
        return score

