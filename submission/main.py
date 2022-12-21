class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Move:
    def __init__(self, start, end):
        self.start = start
        self.end = end
    
    def to_tuple(self):
        return ((self.start.x, self.start.y), (self.end.x, self.end.y))

def copy(board):
    return [[board[i][j] for j in range(0, 5)] for i in range(0, 5)]

def getNeighbors(board, position, playerId):
    neighbors = []
    x = position.x
    y = position.y
    if x > 0:
        if board[x - 1][y] == playerId:
            neighbors.append(Position(x - 1, y))
    if x < 4:
        if board[x + 1][y] == playerId:
            neighbors.append(Position(x + 1, y))
    if y > 0:
        if board[x][y - 1] == playerId:
            neighbors.append(Position(x, y - 1))
    if y < 4:
        if board[x][y + 1] == playerId:
            neighbors.append(Position(x, y + 1))
    if (x + y) % 2 == 0:
        if (x > 0) & (y > 0):
            if board[x - 1][y - 1] == playerId:
                neighbors.append(Position(x - 1, y - 1))
        if (x < 4) & (y > 0):
            if board[x + 1][y - 1] == playerId:
                neighbors.append(Position(x + 1, y - 1))
        if (x < 4) & (y < 4):
            if board[x + 1][y + 1] == playerId:
                neighbors.append(Position(x + 1, y + 1))
        if (x > 0) & (y < 4):
            if board[x - 1][y + 1] == playerId:
                neighbors.append(Position(x - 1, y + 1))
    return neighbors

def canMoveTo(board, position, playerId):
    validPositions = []
    x = position.x
    y = position.y
    if board[x][y] == playerId:
        if x > 0:
            if board[x - 1][y] == 0:
                validPositions.append(Position(x - 1, y))
        if x < 4:
            if board[x + 1][y] == 0:
                validPositions.append(Position(x + 1, y))
        if y > 0:
            if board[x][y - 1] == 0:
                validPositions.append(Position(x, y - 1))
        if y < 4:
            if board[x][y + 1] == 0:
                validPositions.append(Position(x, y + 1))
        if (x + y) % 2 == 0:
            if (x > 0) & (y > 0):
                if board[x - 1][y - 1] == 0:
                    validPositions.append(Position(x - 1, y - 1))
            if (x < 4) & (y > 0):
                if board[x + 1][y - 1] == 0:
                    validPositions.append(Position(x + 1, y - 1))
            if (x < 4) & (y < 4):
                if board[x + 1][y + 1] == 0:
                    validPositions.append(Position(x + 1, y + 1))
            if (x > 0) & (y < 4):
                if board[x - 1][y + 1] == 0:
                    validPositions.append(Position(x - 1, y + 1))
    return validPositions

def isErrorMove(board, move):
    cond1 = (move.start.x == move.end.x) & (move.start.y == move.end.y)
    cond2 = (board[move.end.x][move.end.y] == 1) | (board[move.end.x][move.end.y] == -1)
    cond3 = (move.end.x > move.start.x + 1) | (move.end.y > move.start.y + 1)
    cond4 = (move.start.x < 0) | (move.start.x > 4) | (move.start.y < 0) | (move.start.y > 4) | (move.end.x < 0) | (move.end.y > 4) | (move.end.x < 0) | (move.end.y > 4)
    return cond1 | cond2 | cond3 | cond4

def ganh(board, move, playerId):
    ganhPositions = []
    if isErrorMove(board, move):
        return ganhPositions
    x = move.end.x
    y = move.end.y
    if (x > 0) & (x < 4):
        if (board[x + 1][y] == -playerId) & (board[x - 1][y] == -playerId):
            ganhPositions.append(Position(x + 1, y))
            ganhPositions.append(Position(x - 1, y))
    if (y > 0) & (y < 4):
        if (board[x][y + 1] == -playerId) & (board[x][y - 1] == -playerId):
            ganhPositions.append(Position(x, y + 1))
            ganhPositions.append(Position(x, y - 1))
    if ((x == 1) & (y == 1)) | ((x == 1) & (y == 3)) | ((x == 2) & (y == 2)) | ((x == 3) & (y == 1)) | ((x == 3) & (y == 3)):
        if (board[x - 1][y - 1] == -playerId) & (board[x + 1][y + 1] == -playerId):
            ganhPositions.append(Position(x - 1, y - 1))
            ganhPositions.append(Position(x + 1, y + 1))
        if (board[x + 1][y - 1] == -playerId) & (board[x - 1][y + 1] == -playerId):
            ganhPositions.append(Position(x + 1, y - 1))
            ganhPositions.append(Position(x - 1, y + 1))
    return ganhPositions

def vay(board, move, playerId):
    vayPositions = []
    if isErrorMove(board, move):
        return vayPositions
    clone = copy(board)
    clone[move.start.x][move.start.y] = 0
    clone[move.end.x][move.end.y] = playerId
    flag = True
    while flag:
        count = 0
        for i in range(0, 5):
            isChanged = False
            for j in range(0, 5):
                if (clone[i][j] == -playerId) & (len(canMoveTo(clone, Position(i, j), -playerId)) > 0):
                    clone[i][j] = 0
                    isChanged = True
                    break
                count += 1
            if isChanged:
                break
        if count == 25:
            flag = False
    for i in range(0, 5):
        for j in range(0, 5):
            if clone[i][j] == -playerId:
                vayPositions.append(Position(i, j))
    return vayPositions

def bay(curBoard, preBoard, playerId):
    moveList = []
    prePlayer = preOpp = curPlayer = curOpp = 0
    for i in range(0, 5):
        for j in range(0, 5):
            if preBoard[i][j] == playerId:
                prePlayer += 1
            if preBoard[i][j] == -playerId:
                preOpp += 1
            if curBoard[i][j] == playerId:
                curPlayer += 1
            if curBoard[i][j] == -playerId:
                curOpp += 1
    target = Position(-1, -1)
    for i in range(0, 5):
        isChanged = False
        for j in range(0, 5):
            if (preBoard[i][j] == -playerId) & (curBoard[i][j] == 0):
                target = Position(i, j)
                isChanged = True
                break
        if isChanged:
            break
    if (prePlayer == curPlayer) & (preOpp == curOpp):
        oppNextToPositions = getNeighbors(curBoard, target, playerId)
        if len(oppNextToPositions) == 0:
            return moveList
        else:
            for oppPosition in oppNextToPositions:
                if len(ganh(curBoard, Move(oppPosition, target), playerId)) > 0:
                    moveList.append(Move(oppPosition, target))
    return moveList

def getValidMoves(curBoard, preBoard, playerId):
    validMoves = []
    bayMoves = bay(curBoard, preBoard, playerId)
    if len(bayMoves) != 0:
        validMoves = bayMoves
    else:
        for i in range(0, 5):
            for j in range(0, 5):
                if curBoard[i][j] == playerId:
                    for position in canMoveTo(curBoard, Position(i, j), playerId):
                        validMoves.append(Move(Position(i, j), position))
    return validMoves

def makeMove(board, move, playerId):
    if isErrorMove(board, move):
        print('Error move!')
    else:
        ganhPositions = ganh(board, move, playerId)
        if len(ganhPositions) > 0:
            for pos in ganhPositions:
                board[pos.x][pos.y] = playerId
        vayPositions = vay(board, move, playerId)
        if len(vayPositions) > 0:
            for pos in vayPositions:
                board[pos.x][pos.y] = playerId
        board[move.start.x][move.start.y] = 0
        board[move.end.x][move.end.y] = playerId
    return board

def isWin(board):
    count = sum(sum(board[i]) for i in range(0, 5))
    if abs(count) == 16:
        return True
    else:
        return False

def isNewGame(curBoard, preBoard):
    for i in range(0, 5):
        for j in range(0, 5):
            if curBoard[i][j] != preBoard[i][j]:
                return False
    return True

def isLegal(move):
    return move.start.x * move.start.y * move.end.x * move.end.y != 1

def print_board(board):
    for i in board:
        row = []
        for j in i:
            row.append(label(j))
        print("  ".join(row))



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




def move(prev_board, board, player, remain_time_x, remain_time_o): # khong sua ten ham nay
    agent = MinimaxAgent(2, player)
    move = agent.selectMove(board, prev_board if prev_board is not None else copy(board))
    return move.to_tuple()
    