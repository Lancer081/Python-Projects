import chess
import chess.engine
import chess.polyglot
import time
import math

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


def evaluate_board():
    if board.is_checkmate():
        if board.turn:
            return -math.inf
        else:
            return math.inf
    if board.is_stalemate():
        return 0
    if board.is_insufficient_material():
        return 0

    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))

    material = 100 * (wp - bp) + 320 * (wn - bn) + 330 * (wb - bb) + 500 * (wr - br) + 900 * (wq - bq)

    pawnsq = sum([pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
    pawnsq = pawnsq + sum([-pawntable[chess.square_mirror(i)]
                           for i in board.pieces(chess.PAWN, chess.BLACK)])
    knightsq = sum([knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
    knightsq = knightsq + sum([-knightstable[chess.square_mirror(i)]
                               for i in board.pieces(chess.KNIGHT, chess.BLACK)])
    bishopsq = sum([bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
    bishopsq = bishopsq + sum([-bishopstable[chess.square_mirror(i)]
                               for i in board.pieces(chess.BISHOP, chess.BLACK)])
    rooksq = sum([rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)])
    rooksq = rooksq + sum([-rookstable[chess.square_mirror(i)]
                           for i in board.pieces(chess.ROOK, chess.BLACK)])
    queensq = sum([queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)])
    queensq = queensq + sum([-queenstable[chess.square_mirror(i)]
                             for i in board.pieces(chess.QUEEN, chess.BLACK)])
    kingsq = sum([kingstable[i] for i in board.pieces(chess.KING, chess.WHITE)])
    kingsq = kingsq + sum([-kingstable[chess.square_mirror(i)]
                           for i in board.pieces(chess.KING, chess.BLACK)])

    board.turn = not board.turn
    oppMoveCount = board.legal_moves.count()
    board.turn = not board.turn

    mobility = 10 * (board.legal_moves.count() - oppMoveCount)

    score = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq + mobility

    if board.turn:
        return score
    else:
        return -score


def make_move(mov):
    board.push(mov)
    return mov


def unmake_move():
    mov = board.pop()
    return mov


def quiesce(depth, alpha, beta):
    stand_pat = evaluate_board()

    if depth == 0:
        return stand_pat

    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    for move in board.legal_moves:
        if board.is_capture(move):
            make_move(move)
            score = -quiesce(depth - 1, -beta, -alpha)
            unmake_move()

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
    return alpha


def negamax(depth, alpha, beta):
    global positions

    if depth == 0 or board.is_game_over():
        return quiesce(1, -math.inf, math.inf), None

    bestScore = -math.inf

    for move in board.legal_moves:
        bestMove = move
        break

    for move in board.legal_moves:
        positions += 1

        make_move(move)
        score = -negamax(depth - 1, -beta, -alpha)[0]
        unmake_move()

        if score > bestScore:
            bestScore = score
            bestMove = move

        alpha = max(alpha, bestScore)

        if alpha >= beta:
            break
    return bestScore, bestMove


tpTable = []
board = chess.Board()

positions = 0

engine = chess.engine.SimpleEngine.popen_uci("C:/Users/lance/Desktop/ArenaChess/Engines/stockfish.exe")

while not board.is_game_over():
    if board.turn:
        try:
            move = chess.polyglot.MemoryMappedReader("C:/Users/lance/bookfish.bin").weighted_choice(board).move
            make_move(move)
        except:
            last = time.time()
            score, mov = negamax(4, -math.inf, math.inf)
            now = time.time()
            print("Best move:" + str(move))
            print("Move score:" + str(score))
            print("Positions:" + str(positions))
            print("Evaluation Time:" + str(now - last))
            positions = 0
            make_move(mov)
    else:
        try:
            move = chess.polyglot.MemoryMappedReader("C:/Users/lance/bookfish.bin").weighted_choice(board).move
            make_move(move)
        except:
            last = time.time()
            score, mov = negamax(3, -math.inf, math.inf)
            now = time.time()
            print("Best move:" + str(move))
            print("Move score:" + str(score))
            print("Positions:" + str(positions))
            print("Evaluation Time:" + str(now - last))
            positions = 0
            make_move(mov)

    print(board)
    print("\n")

engine.quit()
