import csv
import time

from board import init_postion, get_legal_moves, serch
from ai import randomai_2
from earch_ai import minimax_ai


def play_one_game(game_number, random_player, depth=3):
    # 初期盤面を作成
    matrix = init_postion(4, 4)

    player = 1
    consecutive_passes = 0
    move_count = 0

    minimax_time = 0.0
    minimax_moves = 0

    while consecutive_passes < 2:
        legal_moves = get_legal_moves(player, matrix)

        # 置ける場所がない場合はパス
        if not legal_moves:
            consecutive_passes += 1
            player = 3 - player
            continue

        consecutive_passes = 0

        # ランダムAIの手番
        if player == random_player:
            position = randomai_2(legal_moves)

        # ミニマックスAIの手番
        else:
            start_time = time.perf_counter()

            position = minimax_ai(matrix, player, depth=depth)

            elapsed = time.perf_counter() - start_time
            minimax_time += elapsed
            minimax_moves += 1

        # 石を置く
        if not serch(position, player, matrix):
            raise RuntimeError(f"試合{game_number}: 不正な着手 {position}")

        move_count += 1
        player = 3 - player

    # 最終的な石の数
    player1_score = int((matrix == 1).sum())
    player2_score = int((matrix == 2).sum())

    # 勝者を判定
    if player1_score > player2_score:
        winner = 1
    elif player2_score > player1_score:
        winner = 2
    else:
        winner = 0  # 引き分け

    # 勝者がランダムAIかミニマックスAIかを判定
    if winner == 0:
        result = "引き分け"
    elif winner == random_player:
        result = "ランダムAI勝利"
    else:
        result = "ミニマックスAI勝利"

    avg_time = minimax_time / minimax_moves if minimax_moves > 0 else 0.0

    return {
        "game": game_number,
        "random_player": random_player,
        "minimax_player": 3 - random_player,
        "winner": winner,
        "result": result,
        "player1_stones": player1_score,
        "player2_stones": player2_score,
        "moves": move_count,
        "minimax_moves": minimax_moves,
        "minimax_total_time_s": minimax_time,
        "minimax_avg_time_s": avg_time,
    }


def main():
    total_games = 100
    depth = 3

    results = []

    # 100試合を自動対戦
    for game_number in range(1, total_games + 1):

        # 先手を交互に変更する
        if game_number % 2 == 1:
            random_player = 1
        else:
            random_player = 2

        result = play_one_game(game_number, random_player, depth)

        results.append(result)

        print(
            f"{game_number:3}/{total_games}試合: "
            f"{result['result']} "
            f"({result['player1_stones']}-"
            f"{result['player2_stones']})"
        )

    # 試合ごとの結果をCSVに保存
    with open("experiment_results.csv", "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    # 勝敗を集計
    minimax_wins = sum(r["result"] == "ミニマックスAI勝利" for r in results)

    random_wins = sum(r["result"] == "ランダムAI勝利" for r in results)

    draws = sum(r["result"] == "引き分け" for r in results)

    avg_time = sum(r["minimax_avg_time_s"] for r in results) / total_games

    total_minimax_time = sum(r["minimax_total_time_s"] for r in results)

    # 全体の集計結果をCSVに保存
    summary = {
        "total_games": total_games,
        "depth": depth,
        "minimax_wins": minimax_wins,
        "random_wins": random_wins,
        "draws": draws,
        "minimax_win_rate_percent": minimax_wins / total_games * 100,
        "random_win_rate_percent": random_wins / total_games * 100,
        "draw_rate_percent": draws / total_games * 100,
        "avg_minimax_time_per_move_s": sum(r["minimax_total_time_s"] for r in results)
        / max(sum(r["minimax_moves"] for r in results), 1),
        "avg_minimax_time_per_game_s": total_minimax_time / total_games,
    }

    with open("experiment_summary.csv", "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=summary.keys())
        writer.writeheader()
        writer.writerow(summary)

    print("\n===== 100試合の集計 =====")
    print(f"ミニマックスAI勝利: {minimax_wins}")
    print(f"ランダムAI勝利:     {random_wins}")
    print(f"引き分け:           {draws}")
    print("ミニマックスAI勝率: " f"{summary['minimax_win_rate_percent']:.1f}%")
    print("1手あたりの平均思考時間: " f"{summary['avg_minimax_time_per_move_s']:.6f}秒")
    print("\nCSVを保存しました。")
    print("experiment_results.csv")
    print("experiment_summary.csv")


if __name__ == "__main__":
    main()
