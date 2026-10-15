import numpy as np


def init_postion(ley, row):
    matrix = np.zeros((ley, row), dtype=np.int8)
    my = ley // 2
    mx = row // 2
    my_1 = (ley // 2) - 1
    mx_1 = (row // 2) - 1
    matrix[my, mx] = 2
    matrix[my_1, mx_1] = 2
    matrix[my, mx_1] = 1
    matrix[my_1, mx] = 1
    print(f"{matrix}初期値")
    return matrix


def serch_change(y, x, dx, dy, new_x, new_y, or1_2, matrix):
    while 0 <= y < len(matrix) and 0 <= x < len(matrix):
        if matrix[y][x] == or1_2 or matrix[y][x] == 0:
            break

        y += dy
        x += dx
    while 0 <= y < len(matrix) and 0 <= x < len(matrix):
        if matrix[y][x] == 0:
            break
        y -= dy
        x -= dx
        matrix[y][x] = or1_2
        if matrix[new_y][new_x] == matrix[y][x]:
            break


search = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def serch(position_list, or1_2, matrix):
    print(position_list)
    mode = 0

    if matrix[position_list[0]][position_list[1]] == 0:
        if or1_2 == 1:
            mlen = 2
        elif or1_2 == 2:
            mlen = 1
        for dy, dx in search:
            new_y = position_list[0] + dy
            new_x = position_list[1] + dx
            if not (0 <= new_y < len(matrix) and 0 <= new_x < len(matrix)):
                continue
            if matrix[new_y][new_x] == mlen:
                y = new_y
                x = new_x
                serch_change(y, x, dx, dy, new_x, new_y, or1_2, matrix)
                if matrix[y][x] == or1_2:
                    matrix[position_list[0]][position_list[1]] = or1_2
    if matrix[position_list[0]][position_list[1]] == or1_2:
        mode = mlen
    else:
        mode = or1_2
    print(matrix)
    return mode


def select(num, pos, mode):
    print(f"{num}回目のターン")
    print(f"{mode}のターン")
    try:
        pos[-1][0] = int(input("Y座標: "))
        pos[-1][1] = int(input("X座標: "))
    except ValueError:

        print(f"値を数値で行いましょう")
    print(f"{pos}置く座標")


def main():
    ley = 6
    row = 6
    matrix = init_postion(ley, row)
    mode = 0
    num = 1
    pos = []

    while True:
        pos.append([None, None])
        if mode == 0:
            select(num, pos, 1)
            mode = serch(pos[-1], 1, matrix)
            print(f"mode{mode}")
        elif mode == 2:
            select(num, pos, 2)
            mode = serch(pos[-1], 2, matrix)
            print(f"mode{mode}")
        else:
            select(num, pos, 1)
            mode = serch(pos[-1], 1, matrix)
            print(f"mode{mode}")
        num += 1


main()
