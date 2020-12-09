import pygame
import math
import random

SQUARE_SIZE = 50
BOARD_SIZE = 8

IMAGES = {}

pawntable = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0]

knightstable = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]

bishopstable = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]

rookstable = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0]

queenstable = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]

kingstable = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]

pygame.init()
size = (SQUARE_SIZE * BOARD_SIZE, SQUARE_SIZE * BOARD_SIZE)
display = pygame.display.set_mode(size)
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

running = True
firstClick = True
staleMate = False
checkMate = False
inCheck = False
moveMade = False

turn = 'w'
selected = ()
moveList = []
pins = []
checks = []
tTable = []
moveScores = []

wKingPos = (7, 4)
bKingPos = (0, 4)

positions = 0
repCount = 0

board = [["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
         ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
         ["--", "--", "--", "--", "--", "--", "--", "--"],
         ["--", "--", "--", "--", "--", "--", "--", "--"],
         ["--", "--", "--", "--", "--", "--", "--", "--"],
         ["--", "--", "--", "--", "--", "--", "--", "--"],
         ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
         ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]


class CastleRights:
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


currentCastleRights = CastleRights(True, True, True, True)
castleRightsLog = [CastleRights(currentCastleRights.wks, currentCastleRights.bks,
                                currentCastleRights.wqs, currentCastleRights.bqs)]


class Move:
    def __init__(self, start, end, isCastleMove=False):
        self.start = start
        self.end = end
        self.startRow = start[0]
        self.startCol = start[1]
        self.endRow = end[0]
        self.endCol = end[1]
        self.capturedPiece = board[self.endRow][self.endCol]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.isPromotion = False
        if (self.pieceMoved == 'wP' and self.endRow == 0) or (
                self.pieceMoved == 'bP' and self.endRow == BOARD_SIZE - 1):
            self.isPromotion = True
        self.isCastleMove = isCastleMove


def drawSquares():
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if (r + c) % 2 == 0:
                pygame.draw.rect(display, pygame.Color("white"),
                                 (SQUARE_SIZE * c, SQUARE_SIZE * r, SQUARE_SIZE, SQUARE_SIZE))
            else:
                pygame.draw.rect(display, pygame.Color("grey"),
                                 (SQUARE_SIZE * c, SQUARE_SIZE * r, SQUARE_SIZE, SQUARE_SIZE))


def drawPieces():
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == "--":
                continue

            pieces = ["bR", "bN", "bB", "bQ", "bK", "wR", "wN", "wB", "wQ", "wK", "bP", "wP"]
            for piece in pieces:
                if board[r][c] == piece:
                    display.blit(IMAGES[piece], (c * SQUARE_SIZE, r * SQUARE_SIZE))


def loadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "wR", "wN", "wB", "wQ", "wK", "bP", "wP"]
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"),
                                               (SQUARE_SIZE, SQUARE_SIZE))


def updateDisplay():
    global turn

    drawSquares()
    drawPieces()

    if selected != ():
        s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
        s.set_alpha(100)
        s.fill(pygame.Color("blue"))
        display.blit(s, (clickCol * SQUARE_SIZE, clickRow * SQUARE_SIZE))
        s.fill(pygame.Color("yellow"))

        piece = board[selected[0]][selected[1]][1]

        if piece != '-':
            validMoves = getValidMoves()
        else:
            return

        for move in validMoves:
            if move.startRow == selected[0] and move.startCol == selected[1]:
                display.blit(s, (move.endCol * SQUARE_SIZE, move.endRow * SQUARE_SIZE))

    pygame.display.update()


def makeMove(move):
    global turn, wKingPos, bKingPos, validMoves

    if move is None:
        print("makeMove error")
        return

    if board[move.startRow][move.startCol][1] == 'K':
        if turn == 'w':
            wKingPos = (move.endRow, move.endCol)
        else:
            bKingPos = (move.endRow, move.endCol)

    board[move.endRow][move.endCol] = board[move.startRow][move.startCol]
    board[move.startRow][move.startCol] = "--"

    if move.isPromotion:
        board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

    moveList.append(move)

    swapTurn()

    if move.isCastleMove:
        if move.endCol + 1 < BOARD_SIZE:
            if move.endCol - move.startCol == 2:  # kingside castle move
                board[move.endRow][move.endCol - 1] = board[move.endRow][move.endCol + 1]  # moves rook
                board[move.endRow][move.endCol + 1] = '--'
            else:  # queenside castle move
                board[move.endRow][move.endCol + 1] = board[move.endRow][move.endCol - 2]
                board[move.endRow][move.endCol - 2] = '--'

    updateCastleRights(move)
    castleRightsLog.append(CastleRights(currentCastleRights.wks, currentCastleRights.bks,
                                        currentCastleRights.wqs, currentCastleRights.bqs))


def undoMove():
    global turn, wKingPos, bKingPos, currentCastleRights, validMoves

    if len(moveList) == 0:
        return

    move = moveList.pop()

    if board[move.endRow][move.endCol][1] == 'K':
        if turn == 'b':
            wKingPos = (move.startRow, move.startCol)
        else:
            bKingPos = (move.startRow, move.startCol)

    board[move.startRow][move.startCol] = board[move.endRow][move.endCol]
    board[move.endRow][move.endCol] = move.capturedPiece

    if move.isPromotion:
        board[move.startRow][move.startCol] = move.pieceMoved[0] + 'P'

    swapTurn()

    castleRightsLog.pop()
    currentCastleRights = castleRightsLog[-1]

    if move.isCastleMove:
        if move.endCol + 1 < BOARD_SIZE:
            if move.endCol - move.startCol == 2:  # kingside
                board[move.endRow][move.endCol + 1] = board[move.endRow][move.endCol - 1]
                board[move.endRow][move.endCol - 1] = '--'
            else:  # queenside
                board[move.endRow][move.endCol - 2] = board[move.endRow][move.endCol + 1]
                board[move.endRow][move.endCol + 1] = "--"


def updateCastleRights(move):
    if move.pieceMoved == 'wK':
        currentCastleRights.wqs = False
        currentCastleRights.wks = False
    elif move.pieceMoved == 'bK':
        currentCastleRights.bqs = False
        currentCastleRights.bks = False
    elif move.pieceMoved == 'wR':
        if move.startRow == 7:
            if move.startCol == 0:
                currentCastleRights.wqs = False
            elif move.startCol == 7:
                currentCastleRights.wks = False
    elif move.pieceMoved == 'bR':
        if move.startRow == 0:
            if move.startCol == 0:
                currentCastleRights.bqs = False
            elif move.startCol == 7:
                currentCastleRights.bks = False


def getPawnMoves(pos):
    piecePinned = False
    pinDir = ()

    for i in range(len(pins) - 1, -1, -1):
        if pins[i][0] == pos[0] and pins[i][1] == pos[1]:
            piecePinned = True
            pinDir = (pins[i][2], pins[i][3])
            pins.remove(pins[i])
            break

    moves = []

    if turn == 'w':
        if board[pos[0] - 1][pos[1]] == "--":
            if not piecePinned or pinDir == (-1, 0):
                moves.append(Move(pos, (pos[0] - 1, pos[1])))
                if pos[0] == 6 and board[pos[0] - 2][pos[1]] == "--":
                    moves.append(Move(pos, (pos[0] - 2, pos[1])))

        if board[pos[0]][pos[1]][0] == turn:
            if 0 <= pos[0] - 1 < BOARD_SIZE and 0 <= pos[1] - 1 < BOARD_SIZE:
                if board[pos[0] - 1][pos[1] - 1][0] == 'b':
                    if not piecePinned or pinDir == (-1, -1):
                        moves.append(Move(pos, (pos[0] - 1, pos[1] - 1)))
            if 0 <= pos[0] - 1 < BOARD_SIZE and 0 <= pos[1] + 1 < BOARD_SIZE:
                if board[pos[0] - 1][pos[1] + 1][0] == 'b':
                    if not piecePinned or pinDir == (-1, 1):
                        moves.append(Move(pos, (pos[0] - 1, pos[1] + 1)))
    else:
        if board[pos[0] + 1][pos[1]] == "--":
            if not piecePinned or pinDir == (1, 0):
                moves.append(Move(pos, (pos[0] + 1, pos[1])))
                if pos[0] == 1 and board[pos[0] + 2][pos[1]] == "--":
                    moves.append(Move(pos, (pos[0] + 2, pos[1])))

        if board[pos[0]][pos[1]][0] == turn:
            if 0 <= pos[0] + 1 < BOARD_SIZE and 0 <= pos[1] - 1 < BOARD_SIZE:
                if board[pos[0] + 1][pos[1] - 1][0] == 'w':
                    if not piecePinned or pinDir == (1, -1):
                        moves.append(Move(pos, (pos[0] + 1, pos[1] - 1)))
            if 0 <= pos[0] + 1 < BOARD_SIZE and 0 <= pos[1] + 1 < BOARD_SIZE:
                if board[pos[0] + 1][pos[1] + 1][0] == 'w':
                    if not piecePinned or pinDir == (1, 1):
                        moves.append(Move(pos, (pos[0] + 1, pos[1] + 1)))

    return moves


def getRookMoves(pos):
    piecePinned = False
    pinDir = ()

    for i in range(len(pins) - 1, -1, -1):
        if pins[i][0] == pos[0] and pins[i][1] == pos[1]:
            piecePinned = True
            pinDir = (pins[i][2], pins[i][3])
            if board[pos[0]][pos[1]][1] != 'Q':
                pins.remove(pins[i])
            break

    moves = []
    rookDirs = ((1, 0), (-1, 0), (0, -1), (0, 1))

    for d in rookDirs:
        for i in range(1, BOARD_SIZE):
            endRow = pos[0] + d[0] * i
            endCol = pos[1] + d[1] * i

            if 0 <= endRow < BOARD_SIZE and 0 <= endCol < BOARD_SIZE:
                if not piecePinned or pinDir == d or pinDir == (-d[0], -d[1]):
                    if board[endRow][endCol] == "--":
                        moves.append(Move(pos, (endRow, endCol)))
                    elif board[endRow][endCol][0] != board[pos[0]][pos[1]][0]:
                        moves.append(Move(pos, (endRow, endCol)))
                        break
                    else:
                        break
            else:
                break

    return moves


def getBishopMoves(pos):
    piecePinned = False
    pinDir = ()

    for i in range(len(pins) - 1, -1, -1):
        if pins[i][0] == pos[0] and pins[i][1] == pos[1]:
            piecePinned = True
            pinDir = (pins[i][2], pins[i][3])
            pins.remove(pins[i])
            break

    moves = []
    bishopDirs = ((1, 1), (-1, -1), (1, -1), (-1, 1))

    for dir in bishopDirs:
        for i in range(1, BOARD_SIZE):
            endRow = pos[0] + dir[0] * i
            endCol = pos[1] + dir[1] * i

            if 0 <= endRow < BOARD_SIZE and 0 <= endCol < BOARD_SIZE:
                if not piecePinned or pinDir == dir or pinDir == (-dir[0], -dir[1]):
                    if board[endRow][endCol] == "--":
                        moves.append(Move(pos, (endRow, endCol)))
                    elif board[endRow][endCol][0] != board[pos[0]][pos[1]][0]:
                        moves.append(Move(pos, (endRow, endCol)))
                        break
                    else:
                        break
            else:
                break

    return moves


def getKnightMoves(pos):
    piecePinned = False

    for i in range(len(pins) - 1, -1, -1):
        if pins[i][0] == pos[0] and pins[i][1] == pos[1]:
            piecePinned = True
            pins.remove(pins[i])
            break

    moves = []
    knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))

    for m in knightMoves:
        endRow = pos[0] + m[0]
        endCol = pos[1] + m[1]
        if 0 <= endRow < BOARD_SIZE and 0 <= endCol < BOARD_SIZE:
            if not piecePinned:
                endPiece = board[endRow][endCol][0]
                if endPiece != turn:
                    moves.append(Move(pos, (endRow, endCol)))

    return moves


def getKingMoves(pos):
    global wKingPos, bKingPos, inCheck, pins, checks

    moves = []
    rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
    colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)

    for i in range(BOARD_SIZE):
        endRow = pos[0] + rowMoves[i]
        endCol = pos[1] + colMoves[i]
        if 0 <= endRow < BOARD_SIZE and 0 <= endCol < BOARD_SIZE:
            endPiece = board[endRow][endCol]
            if endPiece[0] != turn:
                if turn == 'w':
                    wKingPos = (endRow, endCol)
                else:
                    bKingPos = (endRow, endCol)

                pinsAndChecksSave = inCheck, pins, checks

                inCheck, pins, checks = checkForPinsAndChecks()

                if not inCheck:
                    moves.append(Move(pos, (endRow, endCol)))

                inCheck, pins, checks = pinsAndChecksSave

                if turn == 'w':
                    wKingPos = pos
                else:
                    bKingPos = pos

    return moves


def getCastleMoves(pos):
    moves = []

    if isAttacked(pos):
        return

    if (turn == 'w' and currentCastleRights.wks) or (turn == 'b' and currentCastleRights.bks):
        for move in getKingsideCastleMoves(pos):
            moves.append(move)
    if (turn == 'w' and currentCastleRights.wqs) or (turn == 'b' and currentCastleRights.bqs):
        for move in getQueensideCastleMoves(pos):
            moves.append(move)

    return moves


def getKingsideCastleMoves(pos):
    moves = []

    if board[pos[0]][pos[1] + 1] == '--' and board[pos[0]][pos[1] + 2] == '--':
        if not isAttacked((pos[0], pos[1] + 1)) and not isAttacked((pos[0], pos[1] + 2)):
            moves.append(Move(pos, (pos[0], pos[1] + 2), isCastleMove=True))

    return moves


def getQueensideCastleMoves(pos):
    moves = []

    if board[pos[0]][pos[1] - 1] == '--' and board[pos[0]][pos[1] - 2] == '--' and board[pos[0]][pos[1] - 3] == '--':
        if not isAttacked((pos[0], pos[1] - 1)) and not isAttacked((pos[0], pos[1] - 2)):
            moves.append(Move(pos, (pos[0], pos[1] - 2), isCastleMove=True))

    return moves


def getQueenMoves(pos):
    moves = []
    for move in getRookMoves(pos):
        moves.append(move)
    for move in getBishopMoves(pos):
        moves.append(move)
    return moves


def checkForPinsAndChecks():
    global pins, checks, inCheck

    pins = []
    checks = []
    inCheck = False

    if turn == 'w':
        enemyColor = 'b'
        allyColor = 'w'
        startRow = wKingPos[0]
        startCol = wKingPos[1]
    else:
        enemyColor = 'w'
        allyColor = 'b'
        startRow = bKingPos[0]
        startCol = bKingPos[1]

    dirs = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))

    for j in range(len(dirs)):
        d = dirs[j]
        possiblePin = ()

        for i in range(1, BOARD_SIZE):
            endRow = startRow + d[0] * i
            endCol = startCol + d[1] * i

            if 0 <= endRow < BOARD_SIZE and 0 <= endCol < BOARD_SIZE:
                endPiece = board[endRow][endCol]

                if endPiece[0] == allyColor and endPiece[1] != 'K':
                    if possiblePin == ():
                        possiblePin = (endRow, endCol, d[0], d[1])
                    else:
                        break
                elif endPiece[0] == enemyColor:
                    type = endPiece[1]

                    if (0 <= j <= 3 and type == 'R') or \
                            (4 <= j <= 7 and type == 'B') or \
                            (i == 1 and type == 'P' and (
                                    (enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or \
                            (type == 'Q') or (i == 1 and type == 'K'):
                        if possiblePin == ():
                            inCheck = True
                            checks.append((endRow, endCol, d[0], d[1]))
                            break
                        else:
                            pins.append(possiblePin)
                            break
                    else:
                        break
            else:
                break

    knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))

    for m in knightMoves:
        endRow = startRow + m[0]
        endCol = startCol + m[1]

        if 0 <= endRow < BOARD_SIZE and 0 <= endCol < BOARD_SIZE:
            endPiece = board[endRow][endCol]

            if endPiece[0] == enemyColor and endPiece[1] == 'N':
                inCheck = True
                checks.append((endRow, endCol, m[0], m[1]))

    return inCheck, pins, checks


def getAllPossibleMoves():
    moves = []
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            color = board[r][c][0]
            piece = board[r][c][1]
            if color == turn:
                for move in moveGenFuncs[piece]((r, c)):
                    moves.append(move)
    return moves


def isAttacked(pos):
    global turn

    swapTurn()
    moves = getAllPossibleMoves()
    swapTurn()

    for move in moves:
        if move.end == pos:
            return True

    return False


def getValidMoves():
    global checkMate, staleMate, turn, inCheck, pins, checks, currentCastleRights

    currentCastleRightsSave = CastleRights(currentCastleRights.wks, currentCastleRights.bks,
                                           currentCastleRights.wqs, currentCastleRights.bqs)

    inCheck, pins, checks = checkForPinsAndChecks()

    moves = []

    if turn == 'w':
        kingRow = wKingPos[0]
        kingCol = wKingPos[1]

        castleMoves = getCastleMoves(wKingPos)
        if castleMoves is not None:
            for move in castleMoves:
                moves.append(move)
    else:
        kingRow = bKingPos[0]
        kingCol = bKingPos[1]

        castleMoves = getCastleMoves(bKingPos)
        if castleMoves is not None:
            for move in castleMoves:
                moves.append(move)

    if inCheck:
        if len(checks) == 1:
            moves = getAllPossibleMoves()

            check = checks[0]
            checkRow = check[0]
            checkCol = check[1]
            pieceChecking = board[checkRow][checkCol]

            validSquares = []

            if pieceChecking[1] == 'N':
                validSquares = [(checkRow, checkCol)]
            else:
                for i in range(1, BOARD_SIZE):
                    validSquare = (kingRow + check[2] * i, kingCol + check[3] * i)
                    validSquares.append(validSquare)

                    if validSquare[0] == checkRow and validSquare[1] == checkCol:
                        break

            for i in range(len(moves) - 1, -1, -1):
                if moves[i].pieceMoved[1] != 'K':
                    if not (moves[i].endRow, moves[i].endCol) in validSquares:
                        moves.remove(moves[i])
        else:
            for move in getKingMoves((kingRow, kingCol)):
                moves.append(move)
    else:
        for move in getAllPossibleMoves():
            moves.append(move)

    currentCastleRights = currentCastleRightsSave

    return moves


def isTerminalNode():
    validMoves = getValidMoves()
    swapTurn()
    oppValidMoves = getValidMoves()
    swapTurn()

    if len(validMoves) == 0 or len(oppValidMoves) == 0:
        return True

    return False


def reverse(list):
    return [ele for ele in reversed(list)]


def evalPos():
    global turn

    wKs = bKs = wQs = bQs = wNs = bNs = wBs = bBs = wRs = bRs = wPs = bPs = 0
    pawns = knights = bishops = queens = kings = rooks = 0

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c][0] == 'w':
                if board[r][c][1] == "P":
                    wPs += 1
                    pawns += reverse(pawntable)[r * BOARD_SIZE + c]
                elif board[r][c][1] == "N":
                    wNs += 1
                    knights += reverse(knightstable)[r * BOARD_SIZE + c]
                elif board[r][c][1] == "B":
                    wBs += 1
                    bishops += reverse(bishopstable)[r * BOARD_SIZE + c]
                elif board[r][c][1] == "R":
                    wRs += 1
                    rooks += reverse(rookstable)[r * BOARD_SIZE + c]
                elif board[r][c][1] == "Q":
                    wQs += 1
                    queens += reverse(queenstable)[r * BOARD_SIZE + c]
                elif board[r][c][1] == "K":
                    wKs += 1
                    kings += reverse(kingstable)[r * BOARD_SIZE + c]
            else:
                if board[r][c][1] == "P":
                    bPs += 1
                    pawns -= pawntable[r * BOARD_SIZE + c]
                elif board[r][c][1] == "N":
                    bNs += 1
                    knights -= knightstable[r * BOARD_SIZE + c]
                elif board[r][c][1] == "B":
                    bBs += 1
                    bishops -= bishopstable[r * BOARD_SIZE + c]
                elif board[r][c][1] == "R":
                    bRs += 1
                    rooks -= rookstable[r * BOARD_SIZE + c]
                elif board[r][c][1] == "Q":
                    bQs += 1
                    queens -= queenstable[r * BOARD_SIZE + c]
                elif board[r][c][1] == "K":
                    bKs += 1
                    kings -= kingstable[r * BOARD_SIZE + c]

    material = 20000 * (wKs - bKs) + 900 * (wQs - bQs) + 500 * (wRs - bRs) + 300 * (wBs - bBs + wNs - bNs) + 100 * (
                wPs - bPs)

    score = material

    if turn == 'w':
        return score
    else:
        return -score


def getCaptures(moves):
    captures = []

    for move in moves:
        if move.capturedPiece is not None:
            captures.append(move)

    return captures


white_pieces = {
    "P": 0,
    "N": 1,
    "B": 2,
    "R": 3,
    "Q": 4,
    "K": 5
}

black_pieces = {
    "P": 6,
    "N": 7,
    "B": 8,
    "R": 9,
    "Q": 10,
    "K": 11
}


def score_move(move):
    if move.capturedPiece != '--':
        source = 0
        target = 0

        if move.pieceMoved[0] == 'w':
            source = white_pieces[move.pieceMoved[1]]
        else:
            source = black_pieces[move.pieceMoved[1]]

        if move.capturedPiece[0] == 'w':
            target = white_pieces[move.capturedPiece[1]]
        else:
            target = black_pieces[move.capturedPiece[1]]

        return mvv_lva[source][target]

    return 0


def generateHashKey():
    random.seed(256)

    key = random.random()

    key ^= random.random()

    if turn == 'b':
        key *= -1

    return key


mvv_lva = [[
    105, 205, 305, 405, 505, 605, 105, 205, 305, 405, 505, 605,
    104, 204, 304, 404, 504, 604, 104, 204, 304, 404, 504, 604,
    103, 203, 303, 403, 503, 603, 103, 203, 303, 403, 503, 603,
    102, 202, 302, 402, 502, 602, 102, 202, 302, 402, 502, 602,
    101, 201, 301, 401, 501, 601, 101, 201, 301, 401, 501, 601,
    100, 200, 300, 400, 500, 600, 100, 200, 300, 400, 500, 600,

    105, 205, 305, 405, 505, 605, 105, 205, 305, 405, 505, 605,
    104, 204, 304, 404, 504, 604, 104, 204, 304, 404, 504, 604,
    103, 203, 303, 403, 503, 603, 103, 203, 303, 403, 503, 603,
    102, 202, 302, 402, 502, 602, 102, 202, 302, 402, 502, 602,
    101, 201, 301, 401, 501, 601, 101, 201, 301, 401, 501, 601,
    100, 200, 300, 400, 500, 600, 100, 200, 300, 400, 500, 600
]]


def sortMoves(moves):
    move_scores = []

    for move in moves:
        move_scores.append(score_move(move))

    move_scores.sort()

    for current_move in range(len(moves)):
        next_move = current_move + 1

        for next_move in range(len(moves)):
            if move_scores[current_move] < move_scores[next_move]:
                temp_score = move_scores[current_move]
                move_scores[current_move] = move_scores[next_move]
                move_scores[next_move] = temp_score

                temp_move = moves[current_move]
                moves[current_move] = moves[next_move]
                moves[next_move] = temp_move


def negaMax(depth, alpha, beta):
    global turn, positions

    value = -math.inf

    if depth == 0:
        return quiesce(alpha, beta), None

    validMoves = getValidMoves()

    if len(validMoves) == 0:
        if inCheck():
            return -math.inf
        else:
            return 0

    swapTurn()
    if len(getValidMoves()) == 0:
        return math.inf
    swapTurn()

    sortMoves(validMoves)

    bestMove = random.choice(validMoves)

    tableUsed = False

    for move in validMoves:
        positions += 1

        makeMove(move)

        # hashKey = generateHashKey()

        for entry in tTable:
            if entry[0] == board and entry[1] == depth:
                score = entry[2]
                tableUsed = True
                break

        if not tableUsed:
            score = negaMax(depth - 1, -beta, -alpha)[0]
            # tTable.append((bestMove, depth, score))

        undoMove()

        tableUsed = False

        if score > value:
            value = score
            bestMove = move

        alpha = max(alpha, value)

        if alpha >= beta:
            break

    return value, bestMove


def quiesce(alpha, beta):
    global positions

    stand_pat = evalPos()

    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    captures = getCaptures(getValidMoves())

    sortMoves(captures)

    for capture in captures:
        positions += 1

        makeMove(capture)
        score = -quiesce(-beta, -alpha)
        undoMove()

        if score >= beta:
            return beta
        if score > alpha:
            alpha = score

    return alpha


def PVS(depth, alpha, beta):
    global positions

    if depth == 0:
        return quiesce(alpha, beta)

    validMoves = getValidMoves()

    firstMove = validMoves[len(validMoves) - 1]

    makeMove(firstMove)
    bestScore = -PVS(depth - 1, -beta, -alpha)
    undoMove()

    if bestScore > alpha:
        if bestScore >= beta:
            return bestScore
        alpha = bestScore

    validMoves.remove(validMoves[len(validMoves) - 1])

    for move in validMoves:
        makeMove(move)
        score = -PVS(depth - 1, -alpha - 1, -alpha)
        if score > alpha and score < beta:
            score = -PVS(depth - 1, -beta, -alpha)
            if score > alpha:
                alpha = score
        undoMove()
        if score > bestScore:
            if score >= beta:
                return score
            bestScore = score

    return bestScore


def gameOverCheck():
    global turn, running, checkMate, staleMate, board

    validMoves = getValidMoves()

    if len(validMoves) == 0:
        if inCheck:
            checkMate = True
        else:
            staleMate = True

    if checkMate:
        print("Checkmate!")
        checkMate = False
    elif staleMate:
        print("Stalemate!")
        staleMate = False


def swapTurn():
    global turn

    if turn == 'w':
        turn = 'b'
    else:
        turn = 'w'


def getAIMove(depth):
    start = pygame.time.get_ticks()

    # for move in getValidMoves():
    # makeMove(move)
    # score = PVS(depth, -math.inf, math.inf)
    # undoMove()

    # if score > bestScore:
    # bestScore = score
    # bestMove = move

    bestScore, bestMove = negaMax(depth, -math.inf, math.inf)

    end = pygame.time.get_ticks()

    if bestMove is None:
        return

    print("Depth:" + str(depth))
    print("Best Move:" + str(bestMove.start[0]) + str(bestMove.start[1]) + str(bestMove.end[0]) + str(bestMove.end[1]))
    print("Move Score:", bestScore)
    print("Positions Evaluated:", positions)
    print("Evaluation Time:", (end - start) / 1000, "seconds")

    return bestMove


loadImages()
updateDisplay()

moveGenFuncs = {'P': getPawnMoves, 'R': getRookMoves, 'N': getKnightMoves,
                'Q': getQueenMoves, 'K': getKingMoves, 'B': getBishopMoves}

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                undoMove()
                updateDisplay()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            clickRow = mousePos[1] // SQUARE_SIZE
            clickCol = mousePos[0] // SQUARE_SIZE

            if firstClick:
                if board[clickRow][clickCol][0] == turn:
                    selected = (clickRow, clickCol)
                    inCheck, pins, checks = checkForPinsAndChecks()
                    updateDisplay()

                firstClick = False
            else:
                if board[clickRow][clickCol][0] != turn:
                    if selected == (clickRow, clickCol) or selected == ():
                        continue

                    move = Move(selected, (clickRow, clickCol))

                    validMoves = getValidMoves()

                    for m in validMoves:
                        if move.start == m.start and move.end == m.end:
                            makeMove(m)
                            selected = ()
                            gameOverCheck()
                            updateDisplay()
                            moveMade = True
                            break

                    if moveMade:
                        makeMove(getAIMove(5))
                        gameOverCheck()
                        updateDisplay()

                        firstClick = True
                        moveMade = False
                else:
                    selected = ()
                    updateDisplay()
                    firstClick = True

    # while not checkMate and not staleMate:
    # makeMove(getAIMove(2))
    # updateDisplay()
    # gameOverCheck()

    clock.tick(60)

pygame.quit()
quit()
