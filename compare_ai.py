from board import init_postion, get_legal_moves, serch
from hearvest import evaluate_old, evaluate
from earch_ai import minimax_ai


def count_stones(matrix):
    player1 = 0
    player2 = 0

    for row in matrix:
        for cell in row:
            if cell == 1:
                player1 += 1
            elif cell == 2:
                player2 += 1

    return player1, player2


def play_game(old_player=1, depth=3):
    matrix = init_postion()
    current_player = 1

    while True:
        legal_moves = get_legal_moves(current_player, matrix)

        # 合法手がなければパス、両者ともなければ終了
        if not legal_moves:
            opponent = 3 - current_player

            if not get_legal_moves(opponent, matrix):
                break

            current_player = opponent
            continue

        # 旧AIと新AIで評価関数を切り替える
        if current_player == old_player:
            evaluator = evaluate_old
        else:
            evaluator = evaluate

        move = minimax_ai(matrix, current_player, depth, evaluator)

        serch(move, current_player, matrix)

        current_player = 3 - current_player

    p1, p2 = count_stones(matrix)

    if p1 > p2:
        winner = 1
    elif p2 > p1:
        winner = 2
    else:
        winner = 0

    return winner, p1, p2


def main():
    games = 100
    depth = 3

    old_wins = 0
    new_wins = 0
    draws = 0

    for game in range(games):
        # 先手・後手を交互に入れ替える
        old_player = 1 if game % 2 == 0 else 2

        winner, p1, p2 = play_game(old_player, depth)

        if winner == 0:
            draws += 1
        elif winner == old_player:
            old_wins += 1
        else:
            new_wins += 1

        if (game + 1) % 10 == 0:
            print(f"{game + 1}/{games} 試合終了")

    print("\n--- 対戦結果 ---")
    print(f"試合数: {games}")
    print(f"探索深さ: {depth}")
    print(f"旧AIの勝利: {old_wins}")
    print(f"新AIの勝利: {new_wins}")
    print(f"引き分け: {draws}")
    print(f"旧AI勝率: {old_wins / games * 100:.1f}%")
    print(f"新AI勝率: {new_wins / games * 100:.1f}%")


if __name__ == "__main__":
    main()
