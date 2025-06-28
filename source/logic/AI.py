import random
from source.logic.piece import PieceType

def strip_board(board):
    return [[cell.owner if cell is not None else None for cell in row] for row in board]

def drop_piece_sim(board, row, col, piece_type):
    board[row][col] = piece_type

def score_position(board, piece_type):
    score = 0

    center_array = [row[3] for row in board]
    center_count = center_array.count(piece_type)
    score += center_count * 3

    for row in board:
        for c in range(len(row) - 3):
            window = row[c:c + 4]
            score += evaluate_window(window, piece_type)

    for c in range(7):
        col_array = [board[r][c] for r in range(6)]
        for r in range(3):
            window = col_array[r:r + 4]
            score += evaluate_window(window, piece_type)

    for r in range(3):
        for c in range(4):
            window = [board[r + i][c + i] for i in range(4)]
            score += evaluate_window(window, piece_type)

    for r in range(3, 6):
        for c in range(4):
            window = [board[r - i][c + i] for i in range(4)]
            score += evaluate_window(window, piece_type)

    return score

def evaluate_window(window, piece_type):
    opp_piece = PieceType.PLAYER if piece_type == PieceType.ENEMY else PieceType.ENEMY
    score = 0
    if window.count(piece_type) == 4:
        score += 100
    elif window.count(piece_type) == 3 and window.count(None) == 1:
        score += 10
    elif window.count(piece_type) == 2 and window.count(None) == 2:
        score += 5
    elif window.count(opp_piece) == 2 and window.count(None) == 2:
        score -= 25

    if window.count(opp_piece) == 3 and window.count(None) == 1:
        score -= 80

    return score

def get_ai_move(board, is_valid_location, get_next_open_row, drop_piece, winning_move, difficulty):
    valid_locations = [c for c in range(len(board[0])) if is_valid_location(board, c)]
    if not valid_locations:
        return -1

    if difficulty == "easy":
        return random.choice(valid_locations)

    elif difficulty == "medium":
        threat_cols = []
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp = strip_board(board)
            drop_piece_sim(temp, row, col, PieceType.PLAYER)
            if winning_move(temp, PieceType.PLAYER):
                threat_cols.append(col)

        # chance to block if player has next winning move
        if threat_cols and random.random() < 1:
            return random.choice(threat_cols)

        # if not fuck off
        if 3 in valid_locations and random.random() < 0.1:
            return 3

        return random.choice(valid_locations)

    elif difficulty == "hard":
        best_score = -float("inf")
        best_col = random.choice(valid_locations)

        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = strip_board(board)
            drop_piece_sim(temp_board, row, col, PieceType.ENEMY)

            if winning_move(temp_board, PieceType.ENEMY):
                return col

            if winning_move(temp_board, PieceType.PLAYER):
                return col
            else:
                score = score_position(temp_board, PieceType.ENEMY)
                score -= score_position(temp_board, PieceType.PLAYER)

            score = score_position(temp_board, PieceType.ENEMY)
            if score > best_score:
                best_score = score
                best_col = col

        return best_col

    return random.choice(valid_locations)
