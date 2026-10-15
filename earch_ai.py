import random
from board import get_legal_moves, serch
from hearvest import evaluate_old, evaluate_new


def minimax_old(matrix, current_player, ai, depth):
    """旧評価関数を使うMinimax法"""
    legal_moves = get_legal_moves(current_player, matrix)

    if depth == 0:
        return evaluate_old(matrix, ai)

    if not legal_moves:
        opponent = 3 - current_player
        if not get_legal_moves(opponent, matrix):
            return evaluate_old(matrix, ai)
        return minimax_old(matrix, opponent, ai, depth)

    if current_player == ai:
        best = float("-inf")
        for move in legal_moves:
            next_matrix = matrix.copy()
            serch(move, current_player, next_matrix)
            score = minimax_old(next_matrix, 3 - current_player, ai, depth - 1)
            best = max(best, score)
        return best

    best = float("inf")
    for move in legal_moves:
        next_matrix = matrix.copy()
        serch(move, current_player, next_matrix)
        score = minimax_old(next_matrix, 3 - current_player, ai, depth - 1)
        best = min(best, score)
    return best


def minimax_new(matrix, current_player, ai, depth):
    """新評価関数を使うMinimax法"""
    legal_moves = get_legal_moves(current_player, matrix)

    if depth == 0:
        return evaluate_new(matrix, ai)

    if not legal_moves:
        opponent = 3 - current_player
        if not get_legal_moves(opponent, matrix):
            return evaluate_new(matrix, ai)
        return minimax_new(matrix, opponent, ai, depth)

    if current_player == ai:
        best = float("-inf")
        for move in legal_moves:
            next_matrix = matrix.copy()
            serch(move, current_player, next_matrix)
            score = minimax_new(next_matrix, 3 - current_player, ai, depth - 1)
            best = max(best, score)
        return best

    best = float("inf")
    for move in legal_moves:
        next_matrix = matrix.copy()
        serch(move, current_player, next_matrix)
        score = minimax_new(next_matrix, 3 - current_player, ai, depth - 1)
        best = min(best, score)
    return best


def old_ai(matrix, ai, depth=3):
    """旧AIの着手を選ぶ"""
    moves = get_legal_moves(ai, matrix)
    if not moves:
        return None

    best_score = float("-inf")
    best_moves = []

    for move in moves:
        next_matrix = matrix.copy()
        serch(move, ai, next_matrix)
        score = minimax_old(next_matrix, 3 - ai, ai, depth - 1)

        if score > best_score:
            best_score = score
            best_moves = [move]
        elif score == best_score:
            best_moves.append(move)

    return random.choice(best_moves)


def new_ai(matrix, ai, depth=3):
    """新AIの着手を選ぶ"""
    moves = get_legal_moves(ai, matrix)
    if not moves:
        return None

    best_score = float("-inf")
    best_moves = []

    for move in moves:
        next_matrix = matrix.copy()
        serch(move, ai, next_matrix)
        score = minimax_new(next_matrix, 3 - ai, ai, depth - 1)

        if score > best_score:
            best_score = score
            best_moves = [move]
        elif score == best_score:
            best_moves.append(move)

    return random.choice(best_moves)
