import random

from board import get_legal_moves, serch
from hearvest import evaluate_new, evaluate_new_eve5

# 通常の評価関数で使用する初期重み
DEFAULT_WEIGHTS = {
    "stone": 1.75,
    "corner": 12.87,
    "legal": 0.75,
    "edge": 1.92,
}


def minimax_new(matrix, current_player, ai, depth, weights=None):
    """指定した重みで評価するMinimax法"""

    if weights is None:
        weights = DEFAULT_WEIGHTS

    legal_moves = get_legal_moves(current_player, matrix)

    # 探索の深さが0なら盤面を評価する
    if depth == 0:
        return evaluate_new(matrix, ai, weights)

    # 着手できない場合はパス
    if not legal_moves:
        opponent = 3 - current_player

        # 両者とも着手できなければ対局終了
        if not get_legal_moves(opponent, matrix):
            return evaluate_new(matrix, ai, weights)

        # パスでは探索の深さを減らさない
        return minimax_new(matrix, opponent, ai, depth, weights)

    # AIの手番は最大化
    if current_player == ai:
        best = float("-inf")

        for move in legal_moves:
            next_matrix = matrix.copy()
            serch(move, current_player, next_matrix)

            score = minimax_new(
                next_matrix,
                3 - current_player,
                ai,
                depth - 1,
                weights,
            )

            best = max(best, score)

        return best

    # 相手の手番は最小化
    best = float("inf")

    for move in legal_moves:
        next_matrix = matrix.copy()
        serch(move, current_player, next_matrix)

        score = minimax_new(
            next_matrix,
            3 - current_player,
            ai,
            depth - 1,
            weights,
        )

        best = min(best, score)

    return best


def minimax_new_eve5(matrix, current_player, ai, depth):
    """既存のeve5評価関数を使うMinimax法"""

    legal_moves = get_legal_moves(current_player, matrix)

    if depth == 0:
        return evaluate_new_eve5(matrix, ai)

    if not legal_moves:
        opponent = 3 - current_player

        if not get_legal_moves(opponent, matrix):
            return evaluate_new_eve5(matrix, ai)

        return minimax_new_eve5(matrix, opponent, ai, depth)

    if current_player == ai:
        best = float("-inf")

        for move in legal_moves:
            next_matrix = matrix.copy()
            serch(move, current_player, next_matrix)

            score = minimax_new_eve5(
                next_matrix,
                3 - current_player,
                ai,
                depth - 1,
            )

            best = max(best, score)

        return best

    best = float("inf")

    for move in legal_moves:
        next_matrix = matrix.copy()
        serch(move, current_player, next_matrix)

        score = minimax_new_eve5(
            next_matrix,
            3 - current_player,
            ai,
            depth - 1,
        )

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

        # minimax_oldは既存の実装を使用
        score = minimax_old(next_matrix, 3 - ai, ai, depth - 1)

        if score > best_score:
            best_score = score
            best_moves = [move]
        elif score == best_score:
            best_moves.append(move)

    return random.choice(best_moves)


def new_ai(matrix, ai, depth=3, weights=None):
    """指定した重みで新AIの着手を選ぶ"""

    if weights is None:
        weights = DEFAULT_WEIGHTS

    moves = get_legal_moves(ai, matrix)

    if not moves:
        return None

    best_score = float("-inf")
    best_moves = []

    for move in moves:
        next_matrix = matrix.copy()
        serch(move, ai, next_matrix)

        score = minimax_new(
            next_matrix,
            3 - ai,
            ai,
            depth - 1,
            weights,
        )

        if score > best_score:
            best_score = score
            best_moves = [move]
        elif score == best_score:
            best_moves.append(move)

    return random.choice(best_moves)


def new_ai_eve5(matrix, ai, depth=5):
    """既存のeve5評価関数を使うAI"""

    moves = get_legal_moves(ai, matrix)

    if not moves:
        return None

    best_score = float("-inf")
    best_moves = []

    for move in moves:
        next_matrix = matrix.copy()
        serch(move, ai, next_matrix)

        score = minimax_new_eve5(
            next_matrix,
            3 - ai,
            ai,
            depth - 1,
        )

        if score > best_score:
            best_score = score
            best_moves = [move]
        elif score == best_score:
            best_moves.append(move)

    return random.choice(best_moves)
