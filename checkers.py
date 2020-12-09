import pygame as p
import random
import math

#WIN_WIDTH = 575
WIN_WIDTH = 440
WIN_HEIGHT = 467

X_OFFSET = 20
Y_OFFSET = 20

RED = 1
BLACK = 2


class Menu:
    def __init__(self):
        self.switch_pos = (430, 350)
        self.newGame_pos = (430, 380)
        self.solve_pos = (430, 410)

    def draw(self):
        texture = font.render("Switch Color", 1, (255, 255, 255), (0, 0, 255))
        screen.blit(texture, self.switch_pos)

        texture = font.render("New Game", 1, (255, 255, 255), (0, 0, 255))
        screen.blit(texture, self.newGame_pos)

        texture = font.render("Solve", 1, (255, 255, 255), (0, 0, 255))
        screen.blit(texture, self.solve_pos)

    def check_buttons(self, mouse_pos):
        if self.switch_pos[0] <= mouse_pos[0] <= self.switch_pos[0] + 70:  # last addition for these is the button width
            if self.switch_pos[1] <= mouse_pos[1] <= self.switch_pos[1] + font.get_height():
                switch_color()
        if self.newGame_pos[0] <= mouse_pos[0] <= self.newGame_pos[0] + 145:
            if self.newGame_pos[1] <= mouse_pos[1] <= self.newGame_pos[1] + font.get_height():
                restart()
        if self.solve_pos[0] <= mouse_pos[0] <= self.solve_pos[0] + 75:
            if self.solve_pos[1] <= mouse_pos[1] <= self.solve_pos[1] + font.get_height():
                pass


class Move:
    def __init__(self, startRow, startCol, endRow, endCol):
        self.startRow = startRow
        self.startCol = startCol
        self.endRow = endRow
        self.endCol = endCol
        self.start = (startRow, startCol)
        self.end = (endRow, endCol)
        self.capturedPiece = None
        self.isDoubleJump = False


class Piece:
    def __init__(self, color):
        self.color = color
        self.is_king = False


class Square:
    def __init__(self, color):
        self.color = color
        self.piece = None


class Board:
    def __init__(self, w, h, sq_size):
        self.w = w
        self.h = h
        self.sq_size = sq_size
        self.sq = [[Square(RED if (j + i) % 2 == 0 else BLACK) for j in range(self.w)] for i in range(self.h)]

        # Setup Pieces
        for r in range(self.w):
            for c in range(self.h):
                if self.sq[r][c].color == BLACK:
                    if r < 3:
                        self.sq[r][c].piece = Piece(RED)
                    if r > 4:
                        self.sq[r][c].piece = Piece(BLACK)

    def draw(self):
        global status_text, selected

        for r in range(self.w):
            for c in range(self.h):
                rect = (X_OFFSET + c * self.sq_size, Y_OFFSET + r * self.sq_size, self.sq_size, self.sq_size)

                # Draw Squares
                if self.sq[r][c].color == RED:
                    p.draw.rect(screen, (255, 0, 0), rect)
                else:
                    p.draw.rect(screen, (0, 0, 0), rect)

                # Draw Pieces
                radius = self.sq_size // 2
                pos = (X_OFFSET + c * self.sq_size + radius, Y_OFFSET + r * self.sq_size + radius)

                if self.sq[r][c].piece is not None:
                    p.draw.circle(screen, (255, 255, 255), pos, radius - 4)

                    if self.sq[r][c].piece.is_king:
                        if self.sq[r][c].piece.color == RED:
                            p.draw.circle(screen, (255, 0, 0), pos, radius - 5)
                        else:
                            p.draw.circle(screen, (0, 0, 0), pos, radius - 5)

                        tex = font.render("K", 1, (255, 255, 255))
                        screen.blit(tex, (pos[0] - 8, pos[1] - 13))
                    else:
                        if self.sq[r][c].piece.color == RED:
                            p.draw.circle(screen, (255, 0, 0), pos, radius - 5)
                        else:
                            p.draw.circle(screen, (0, 0, 0), pos, radius - 5)


def switch_color():
    for r in range(b.w):
        for c in range(b.h):
            if b.sq[r][c].piece is not None:
                if b.sq[r][c].piece.color == RED:
                    b.sq[r][c].piece = Piece(BLACK)
                else:
                    b.sq[r][c].piece = Piece(RED)


def draw_status():
    tex = font.render(status_text, 1, (255, 255, 255))
    screen.blit(tex, (X_OFFSET, Y_OFFSET + b.sq_size * b.w + 10))


def highlight_square(r, c, color):
    p.draw.rect(screen, color, (X_OFFSET + c * b.sq_size, Y_OFFSET + r * b.sq_size, b.sq_size, b.sq_size), 2)


def is_valid_selection(selection):
    if 0 <= selection[0] < b.w and 0 <= selection[1] < b.h:
        return True
    return False


def get_valid_moves(loc):
    valid_moves = []
    dest = [(loc[0] + 2, loc[1] + 2), (loc[0] - 2, loc[1] - 2), (loc[0] + 2, loc[1] - 2), (loc[0] - 2, loc[1] + 2)]

    for d in dest:
        move = Move(loc[0], loc[1], d[0], d[1])
        if is_valid_selection(d):
            if is_valid_move(move):
                valid_moves.append(move)

    if len(valid_moves) > 0:
        return valid_moves

    dest = [(loc[0] + 1, loc[1] + 1), (loc[0] - 1, loc[1] - 1), (loc[0] + 1, loc[1] - 1), (loc[0] - 1, loc[1] + 1)]

    for d in dest:
        if is_valid_selection(d):
            move = Move(loc[0], loc[1], d[0], d[1])
            if is_valid_move(move):
                valid_moves.append(move)

    return valid_moves


def get_all_valid_moves(color):
    valid_moves = []

    for r in range(b.w):
        for c in range(b.h):
            if b.sq[r][c].piece is not None and b.sq[r][c].piece.color == color:
                moves = get_valid_moves((r, c))
                for move in moves:
                    valid_moves.append(move)

    return valid_moves


def is_valid_move(move):
    loc_square = b.sq[move.startRow][move.startCol]
    dest_square = b.sq[move.endRow][move.endCol]
    middle_square = b.sq[(move.startRow + move.endRow) // 2][(move.startCol + move.endCol) // 2]

    if dest_square.color == RED:
        return False

    if dest_square.piece is not None:
        return False

    if not is_jump(move):
        if must_jump:
            return False
        if abs(move.startRow - move.endRow) > 1 or abs(move.startCol - move.endCol) > 1:
            return False
    else:
        if middle_square.piece is None:
            return False
        if middle_square.piece.color == turn:
            return False

    if loc_square.piece is not None and not loc_square.piece.is_king:
        if turn == RED:
            if move.endRow < move.startRow:
                return False
        else:
            if move.endRow > move.startRow:
                return False

    return True


def is_jump(move):
    return abs(move.startRow - move.endRow) == 2 or abs(move.startCol - move.endCol) == 2


def make_move(move):
    global turn, status_text, red_captures, black_captures
    
    dest_square = b.sq[move.endRow][move.endCol]
    loc_square = b.sq[move.startRow][move.startCol]
    middle_square = b.sq[(move.startRow + move.endRow) // 2][(move.startCol + move.endCol) // 2]

    if is_jump(move):
        # remove jumped piece
        move.capturedPiece = middle_square.piece
        middle_square.piece = None

        if turn == RED:
            red_captures += 1
        else:
            black_captures += 1

        valid_moves = get_valid_moves(move.end)

        # if double jump...
        if len(valid_moves) > 0 and is_jump(valid_moves[0]):
            valid_moves[0].isDoubleJump = True

            dest_square.piece = loc_square.piece
            loc_square.piece = None

            if dest_square.piece is not None:
                if move.endRow == 0 or move.endRow == b.h - 1:
                    dest_square.piece.is_king = True

            move_list.append(valid_moves[0])
            make_move(valid_moves[0])
            status_text = "Double jump!"
            draw_game()
            p.display.update()
            p.time.delay(1000)
            return

    dest_square.piece = loc_square.piece
    loc_square.piece = None

    if dest_square.piece is not None:
        if move.endRow == 0 or move.endRow == b.h - 1:
            dest_square.piece.is_king = True

    status_text = "BLACK's Turn" if turn == RED else "RED's Turn"
    turn = BLACK if turn == RED else RED

    move_list.append(move)


def undo_move():
    global turn, red_captures, black_captures

    if len(move_list) == 0:
        return

    move = move_list.pop()

    dest_square = b.sq[move.endRow][move.endCol]
    loc_square = b.sq[move.startRow][move.startCol]
    middle_square = b.sq[(move.startRow + move.endRow) // 2][(move.startCol + move.endCol) // 2]

    if move.isDoubleJump:
        undo_move()

    if is_jump(move):
        middle_square.piece = move.capturedPiece

        if turn == RED:
            red_captures -= 1
        else:
            black_captures -= 1

    if dest_square.piece is not None:
        if move.endRow == 0 or move.endRow == b.h - 1:
            dest_square.piece.is_king = False

    loc_square.piece = dest_square.piece
    dest_square.piece = None

    turn = BLACK if turn == RED else RED


def make_random_move():
    global must_jump

    jumps = []
    moves = get_all_valid_moves(turn)

    for move in get_all_valid_moves(turn):
        if is_jump(move) and is_valid_move(move):
            jumps.append(move)

    if len(jumps) > 0:
        rand_move = random.choice(jumps)
        make_move(rand_move)
        must_jump = False
    elif len(moves) > 0:
        rand_move = random.choice(moves)
        make_move(rand_move)


def is_won():
    valid_moves = get_all_valid_moves(BLACK if turn == RED else RED)

    if len(valid_moves) == 0:
        return True

    return False


def evaluate():
    valid_moves = get_all_valid_moves(turn)

    if len(valid_moves) == 0:
        return -math.inf

    valid_moves = get_all_valid_moves(BLACK if turn == RED else RED)

    if len(valid_moves) == 0:
        return math.inf

    if turn == RED:
        return red_captures
    else:
        return black_captures


def is_terminal():
    return get_all_valid_moves(turn) == 0 or get_all_valid_moves(BLACK if turn == RED else RED) == 0


def negamax(depth, alpha, beta):
    global positions, turn, red_captures, black_captures

    if depth == 0 or is_terminal():
        return evaluate(), None

    value = -math.inf

    valid_moves = get_all_valid_moves(turn)

    if len(valid_moves) > 0:
        best_move = random.choice(valid_moves)

    for move in valid_moves:
        positions += 1

        red_captures_save = red_captures
        black_captures_save = black_captures

        make_move(move)
        score = -negamax(depth - 1, -beta, -alpha)[0]
        undo_move()

        red_captures = red_captures_save
        black_captures = black_captures_save

        if score > value:
            value = score
            best_move = move

        alpha = max(alpha, value)

        if alpha >= beta:
            break

    return score, best_move


def restart():
    global status_text, turn, selected, b, black_captures, red_captures

    status_text = "RED Won!" if turn == BLACK else "BLACK Won!"

    draw_game()

    p.display.update()
    p.time.delay(3000)

    b = Board(8, 8, 50)

    draw_game()

    turn = BLACK
    selected = (-1, -1)
    black_captures = 0
    red_captures = 0
    move_list.clear()


def draw_game():
    screen.fill((0, 100, 155))
    b.draw()
    draw_status()
    #menu.draw()
    #menu.check_buttons(p.mouse.get_pos())


def draw_valid_moves(selected):
    valid_moves = get_valid_moves(selected)

    for move in valid_moves:
        highlight_square(move.endRow, move.endCol, (0, 255, 0))

        if is_jump(move):
            valid_moves = get_valid_moves(move.end)
            for move in valid_moves:
                if is_jump(move):
                    highlight_square(move.endRow, move.endCol, (0, 255, 0))


def make_AI_move():
    global positions

    past = p.time.get_ticks()
    score, best_move = negamax(3, -math.inf, math.inf)
    now = p.time.get_ticks()

    print("Move Score:", score)
    print("Positions Evaluated:", positions)
    print("Eval time:", (now - past) / 1000)

    positions = 0

    #jumps = []
    #moves = get_all_valid_moves(turn)

    #for move in moves:
    #    if is_jump(move) and is_valid_move(move):
    #        jumps.append(move)

    #if len(jumps) > 0:
    #    rand_move = random.choice(jumps)
    #    make_move(rand_move)
    #elif len(moves) > 0:
    #    rand_move = random.choice(moves)
    #    make_move(rand_move)

    make_move(best_move)


p.init()
screen = p.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
p.display.set_caption("Checkers")

running = True
second_click = False
must_jump = False
multiple_jumps = False

turn = BLACK
selected = (-1, -1)

font = p.sysfont.SysFont("Helvetica", 24)
status_text = "BLACK's Turn"

red_captures = 0
black_captures = 0
positions = 0

move_list = []

b = Board(8, 8, 50)
#menu = Menu()

draw_game()

while running:
    for e in p.event.get():
        if e.type == p.QUIT:
            running = False
        if e.type == p.KEYDOWN:
            if e.key == p.K_q:
                running = False
            if e.key == p.K_z:
                if len(move_list) > 0:
                    undo_move()
                    draw_game()
        if e.type == p.MOUSEBUTTONDOWN:
            mouse_pos = p.mouse.get_pos()

            draw_game()

            if not second_click:
                s = ((mouse_pos[1] - Y_OFFSET) // b.sq_size, (mouse_pos[0] - X_OFFSET) // b.sq_size)

                if is_valid_selection(s):
                    valid_moves = get_all_valid_moves(turn)
                    if len(valid_moves) > 0:
                        if is_jump(valid_moves[0]):
                            must_jump = True

                    if b.sq[s[0]][s[1]].color == BLACK:
                        if b.sq[s[0]][s[1]].piece is not None and b.sq[s[0]][s[1]].piece.color == turn:
                            selected = s
                            highlight_square(selected[0], selected[1], (255, 255, 0))
                            draw_valid_moves(selected)
                else:
                    selected = (-1, -1)
                    continue

                second_click = True
            else:
                dest = ((mouse_pos[1] - Y_OFFSET) // b.sq_size, (mouse_pos[0] - X_OFFSET) // b.sq_size)

                if is_valid_selection(dest):
                    move = Move(selected[0], selected[1], dest[0], dest[1])

                    if is_valid_move(move):
                        make_move(move)
                        must_jump = False

                        # check for game over
                        if is_won():
                            restart()
                            continue

                        selected = (-1, -1)

                        draw_game()
                        p.display.update()

                        make_AI_move()
                        must_jump = False

                        if is_won():
                            restart()
                            continue

                        draw_game()

                selected = (-1, -1)
                second_click = False

    p.display.update()

p.quit()
