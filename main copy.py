from board import init_postion, get_legal_moves, serch, show_board
from ai import randomai_1


def select(num, player, legal_moves):
    """プレイヤーから座標を入力してもらう"""
    print(f"\n{num}回目のターン")
    if player == 1:
        print(f"プレイヤー {player} のターン")
        print(f"置ける場所: {legal_moves}")

        while True:
            try:
                y = int(input("Y座標: "))
                x = int(input("X座標: "))
            except ValueError:
                print("座標は数値で入力してください。")
                continue

            if (y, x) in legal_moves:
                return [y, x]
            print("そこには置けません。別の座標を入力してください。")
    else:
        print(f"置ける場所: {legal_moves}")
        return randomai_1(legal_moves)


def main():
    ley = 4
    row = 4

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

        position = select(num, player, legal_moves)

        if serch(position, player, matrix):
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


if __name__ == "__main__":
    main()
