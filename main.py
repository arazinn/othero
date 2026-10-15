from board import init_postion, get_legal_moves, serch, show_board
from ai import randomai_1, randomai_2
from earch_ai import old_ai, new_ai
import csv
import json

history = []


def select(num, player, legal_moves, matrix):
    """プレイヤーから座標を入力してもらう"""
    print(f"\n{num}回目のターン")

    if player == 1:
        print(f"置ける場所: {legal_moves}")
        return new_ai(matrix, player, depth=3)
    else:
        print(f"置ける場所: {legal_moves}")
        return new_ai(matrix, player, depth=3)


def main():
    ley = 8
    row = 8

    matrix = init_postion(ley, row)

    player = 1
    num = 1
    consecutive_passes = 0

    while consecutive_passes < 2:
        show_board(matrix)

        # 現在のプレイヤーが置ける場所を取得
        legal_moves = get_legal_moves(player, matrix)

        if not legal_moves:
            print(f"プレイヤー {player} は置ける場所がありません。パスします。")

            consecutive_passes += 1
            player = 3 - player
            num += 1
            continue

        # 石を置けた場合は連続パスをリセット
        consecutive_passes = 0

        position = select(num, player, legal_moves, matrix)

        if serch(position, player, matrix):
            player1_score = int((matrix == 1).sum())
            player2_score = int((matrix == 2).sum())

            # 現在の手番を担当したBotを記録
            bot_name = "randomai_2" if player == 1 else "randomai_1"

            # 対戦データを保存
            history.append(
                {
                    "turn": num,
                    "player": player,
                    "y": position[0],
                    "x": position[1],
                    "player1_stones": player1_score,
                    "player2_stones": player2_score,
                    "board": json.dumps(matrix.tolist()),
                }
            )

            player = 3 - player
            num += 1

    # ゲーム終了
    show_board(matrix)

    player1_score = int((matrix == 1).sum())
    player2_score = int((matrix == 2).sum())

    print("\nゲーム終了")
    print(f"プレイヤー1: {player1_score}個")
    print(f"プレイヤー2: {player2_score}個")

    if player1_score > player2_score:
        print("プレイヤー1の勝利")
    elif player2_score > player1_score:
        print("プレイヤー2の勝利")
    else:
        print("引き分け")

    # 勝敗を記録
    if player1_score > player2_score:
        result = "player1_win"
    elif player2_score > player1_score:
        result = "player2_win"
    else:
        result = "draw"

    # 全ターンに最終結果を追加
    for record in history:
        record["result"] = result

    # CSVファイルに保存
    if history:
        with open("history.csv", "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.DictWriter(file, fieldnames=history[0].keys())
            writer.writeheader()
            writer.writerows(history)

        print("対戦データを history.csv に保存しました。")


if __name__ == "__main__":
    main()
