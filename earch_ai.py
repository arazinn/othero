from board import get_legal_moves, serch
from hearvest import evaluate
import random


def minimax(matrix, current_player, ai, depth):
    # 1. 現在のプレイヤーが置ける場所を取得
    legal_moves = get_legal_moves(current_player, matrix)

    # 2. 探索の深さが0なら評価値を返す
    if depth == 0:
        return evaluate(matrix, ai)

    # 3. 合法手がない場合
    if not legal_moves:
        opponent = 3 - current_player
        opponent_moves = get_legal_moves(opponent, matrix)

        # 両者とも置けない場合はゲーム終了
        if not opponent_moves:
            return evaluate(matrix, ai)

        # パスして相手の手番へ（深さは減らさない）
        return minimax(matrix, opponent, ai, depth)

    # 4. AIの手番：MAX
    if current_player == ai:
        best_score = float("-inf")

        for move in legal_moves:
            next_matrix = matrix.copy()
            serch(move, current_player, next_matrix)

            score = minimax(next_matrix, 3 - current_player, ai, depth - 1)

            if score > best_score:
                best_score = score

        return best_score

    # 5. 相手の手番：MIN
    else:
        best_score = float("inf")

        for move in legal_moves:
            next_matrix = matrix.copy()
            serch(move, current_player, next_matrix)

            score = minimax(next_matrix, 3 - current_player, ai, depth - 1)

            if score < best_score:
                best_score = score

        return best_score


def minimax_ai(matrix, ai, depth=3):
    # 1. AIが置ける場所を取得する
    legal_moves = get_legal_moves(ai, matrix)

    # 2. 置ける場所がなければパスする
    if not legal_moves:
        return None

    # 3. 最高評価値と候補手を初期化する
    best_score = float("-inf")
    best_moves = []

    # 4. すべての合法手を試す
    for move in legal_moves:
        next_matrix = matrix.copy()
        serch(move, ai, next_matrix)

        # 5. 着手後の盤面から先を探索する
        score = minimax(next_matrix, 3 - ai, ai, depth - 1)

        # 6. 最高評価値を更新する
        if score > best_score:
            best_score = score
            best_moves = [move]

        # 同じ最高評価値なら候補に追加する
        elif score == best_score:
            best_moves.append(move)

    # 7. 最高評価値の候補から一つ選ぶ
    return list(random.choice(best_moves))
