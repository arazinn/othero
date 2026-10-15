from board import init_postion, get_legal_moves, serch, show_board
import random


def randomai_1(legal_move):

    legal_list = legal_move
    # 置ける場所がなければ何もしない
    if not legal_list:
        return None

    # 合法手からランダムに1手選ぶ
    random_move = random.choice(legal_list)

    return [random_move[0], random_move[1]]


def randomai_2(legal_move):

    legal_list = legal_move
    # 置ける場所がなければ何もしない
    if not legal_list:
        return None

    # 合法手からランダムに1手選ぶ
    random_move = random.choice(legal_list)

    return [random_move[0], random_move[1]]
