import numpy as np

# 8方向（縦・横・斜め）
search = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def init_postion(ley, row):
    """初期盤面を生成する"""
    matrix = np.zeros((ley, row), dtype=np.int8)

    my = ley // 2
    mx = row // 2
    my_1 = my - 1
    mx_1 = mx - 1

    matrix[my, mx] = 2
    matrix[my_1, mx_1] = 2
    matrix[my, mx_1] = 1
    matrix[my_1, mx] = 1

    return matrix


def serch_change(y, x, dx, dy, player, matrix):
    """指定した方向でひっくり返せる石の座標を取得する"""
    height, width = matrix.shape
    opponent = 3 - player
    flips = []

    while 0 <= y < height and 0 <= x < width:
        value = matrix[y, x]

        if value == opponent:
            flips.append((y, x))
        elif value == player:
            # 相手の石を挟めている場合だけ有効
            return flips if flips else []

        else:
            # 空きマスに到達した場合は無効
            return []

        y += dy
        x += dx

    # 盤面の外に出た場合は無効
    return []


def get_flips(y, x, player, matrix):
    """その場所に置いた場合にひっくり返る石を取得する"""
    height, width = matrix.shape

    if not (0 <= y < height and 0 <= x < width):
        return []

    if matrix[y, x] != 0:
        return []

    flips = []

    for dy, dx in search:
        next_y = y + dy
        next_x = x + dx

        direction_flips = serch_change(next_y, next_x, dx, dy, player, matrix)
        flips.extend(direction_flips)

    return flips


def get_legal_moves(player, matrix):
    """プレイヤーが石を置ける座標をすべて取得する"""
    height, width = matrix.shape
    moves = []

    for y in range(height):
        for x in range(width):
            if get_flips(y, x, player, matrix):
                moves.append((y, x))

    return moves


def serch(position_list, player, matrix):
    """指定した座標に石を置き、挟んだ石をひっくり返す"""
    y, x = position_list

    flips = get_flips(y, x, player, matrix)

    if not flips:
        return False

    matrix[y, x] = player

    for flip_y, flip_x in flips:
        matrix[flip_y, flip_x] = player

    return True


def show_board(matrix):
    """盤面を表示する"""
    print("   " + " ".join(map(str, range(matrix.shape[1]))))

    for y, row in enumerate(matrix):
        print(f"{y}: " + " ".join(map(str, row)))
